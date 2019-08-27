#!/usr/bin/python
# this script generates pbs file for each sample replicate
# pbs files are generated and submitted

import sys
sys.path.append('../utils')
sys.path.append('../dnaseq-pipelines/src')

import myUtils as mu
import check as check
import variantCall as vc

import subprocess
import os
import re

inFile1 = 'intermediate/vc-catalog.txt'
pipeline = 'pipeline1-calls'

numThreads=str(4)

pbs = '/'.join([pipeline,'prefix.pbs']) 
reference='/home/bankhead/bt/annotation/gencode/GRCh38-v29/GRCh38.primary_assembly.genome.fa'

(records1,header1,keys1) = mu.readRecords(inFile1,['caller','sampleReplicate','interval'])
# keys1 = keys1[:3]

runLocal = False
submit = True
pars = {'pipeline':pipeline,'threads':numThreads, 'reference':reference}

for key in keys1:
    record = records1[key]
    pars['record'] = record

    sampleReplicate,normal,intervalNum,caller = record['sampleReplicate'],record['normal'],record['intervalNum'],record['caller']

    uName = '_'.join([sampleReplicate,normal,intervalNum,caller])
    pars['uName'] = uName

    # create a script to be executed from job array
    script = '/'.join([pipeline,'scripts',uName + '.sh']) 

    with open(script,'w') as out1:
        # update pars dictionary
        pars['sampleReplicate'] = sampleReplicate
        pars['out'] = out1

        # write yo header
        pars['out'].write('#!/bin/bash\n')

        pars['flavor'] = 'mutect2-tn' if caller == 'mutect2' else 'muse'
        vc.vc(pars)

        # *** check to make sure sample has not already been successfully run ***
#        pars['flavor'] = 'standard'
#        check.isCompleted(pars)

    # update permissions
    cmd = 'chmod 755 ' + script
    subprocess.check_call(cmd,shell=True) 

# execute script
if runLocal:
    print script
#    subprocess.check_call(script,shell=True)
else:
    cmd = 'qsub -o ' + pipeline + '/logs -N ' + pipeline + ' ' + pbs
    print cmd

    if submit:
        subprocess.check_call(cmd,shell=True)
