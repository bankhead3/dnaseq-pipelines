#!/usr/bin/python
# this script generates pbs file for each sample replicate
# pbs files are generated and submitted

import sys
sys.path.append('utils')
sys.path.append('utils/rnaseq-pipelines')

import myUtils as mu
import preprocess as pp
import combine as c
import clean as cl
import align as a
import quantify as q
import count as co
import discover as d
import qc as qc
import check as check
import download as d
import bam2fastq as bf

import subprocess
import os
import re

inFile1 = 'intermediate/fastq-catalog.txt'
inFile2 = 'intermediate/sample-replicate-catalog.txt'
pipeline = 'pipeline1b'
end = 'single'
stranded = True

numThreads=str(8)

pbs = '/'.join([pipeline,'prefix.pbs']) 
gtf = '/nfs/turbo/topBfx/annotation/ucsc-table/GRCh38/refgene-20170605/refGene-sorted-canonical.gtf'
alignerIndexDir='/nfs/turbo/topBfx/annotation/aligner-indexes/star/GRCh38'

(records1,header1,keys1) = mu.readRecords(inFile1,['uniqueName','read'])
(records2,header2,keys2) = mu.readRecords(inFile2,['sampleReplicate'])

pars = {'pipeline':pipeline,'threads':numThreads, 'alignerIndexDir':alignerIndexDir, 'end':end, 'records':records1, 'stranded':stranded, 'gtf':gtf}

for sampleReplicate in keys2:

    # create a script to be executed from job array
    script = '/'.join([pipeline,'scripts',sampleReplicate + '.sh']) 
    with open(script,'w') as out1:
        # update pars dictionary
        pars['sampleReplicate'] = sampleReplicate
        pars['out'] = out1

        # write yo header
        pars['out'].write('#!/bin/bash\n')

        # *** 02 preprocess ***
        pars['flavor'] = 'normal'
        pars['flavor'] = 'skip'
        pp.preprocess(pars)

        # *** 03 combine ***
        pars['flavor'] = 'combine'
#        pars['flavor'] = 'skip'
        c.combine(pars)

        # *** 04 align *** 
        pars['flavor'] = 'star'
#        pars['flavor'] = 'skip' 
        a.align(pars) 

        # *** 05 quantify ***
        pars['flavor'] = 'cufflinks'
#        pars['flavor'] = 'skip'
        q.quantify(pars)

        pars['flavor'] = 'featureCounts'
        co.count(pars)

        # *** 10 qc ***
        pars['flavor'] = 'qorts'
        qc.qc(pars)

        # *** 20 clean *** 
        pars['flavor'] = 'sequencingCore'
        cl.clean(pars) 

        # *** check to make sure sample has not already been successfully run ***
#        pars['flavor'] = 'salmon-bias'
#        check.isCompleted(pars)

        # *** 00 download from gdc portal
#        pars['flavor'] = 'gdc'
#        pars['flavor'] = 'skip'  # for testing
#        d.download(pars)

        # *** 01 extract to fastq files ***
#        pars['flavor'] = 'bam2fastq'
#        pars['flavor'] = 'skip'  # for testing
#        bf.bam2fastq(pars)

    # update permissions
    cmd = 'chmod 755 ' + script
    subprocess.check_call(cmd,shell=True) 

# execute script
cmd = 'qsub -o ' + pipeline + '/logs -N ' + pipeline + ' ' + pbs
print cmd
subprocess.check_call(cmd,shell=True)
