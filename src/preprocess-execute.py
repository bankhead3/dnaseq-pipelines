#!/usr/bin/python
# this script generates pbs file for each sample replicate
# pbs files are generated and submitted

import sys
sys.path.append('../utils')
sys.path.append('../dnaseq-pipelines/src')

import myUtils as mu
import preprocess as pp
import combine as c
import clean as cl
import align as a
import postprocess as pop
import check as check
import qc as qc
import variantCall as vc

import subprocess
import os
import re

inFile1 = 'intermediate/fastq-catalog.txt'
inFile2 = 'intermediate/sample-replicate-catalog-1.txt'
pipeline = 'pipeline1'
end = 'paired'
stranded = True

numThreads=str(12)

pbs = '/'.join([pipeline,'prefix.pbs']) 
gtf = '/nfs/turbo/topBfx/annotation/ucsc-table/GRCh38/refgene-20170605/refGene-sorted-canonical.gtf'
alignerIndexDir='/nfs/turbo/topBfx/annotation/aligner-indexes/star/GRCh38'
alignerIndex='/nfs/turbo/bankheadTurbo/annotation/aligner-indexes/bwa/GRCh38/0.7.15/GRCh38.primary_assembly.genome.fa'
reference='/home/bankhead/bt/annotation/gencode/GRCh38-v29/GRCh38.primary_assembly.genome.fa'
known1 = '/home/bankhead/bt/annotation/variants/dbsnp/Homo_sapiens_assembly38.dbsnp138.vcf'
known2 = '/home/bankhead/bt/annotation/variants/Mills_and_1000G_gold_standard.indels.hg38.vcf'
bed = '/home/bankhead/bt/annotation/coverage/idt/xGenExomeResearchPanelv1.0/xgen-exome-research-panel-targetsae255a1532796e2eaa53ff00001c1b3c.bed'
bed = '/home/bankhead/bt/annotation/gencode/GRCh38-v29/exons-protein-coding.bed'

(records1,header1,keys1) = mu.readRecords(inFile1,['uniqueName','read'])
(records2,header2,keys2) = mu.readRecords(inFile2,['sampleReplicate'])

fastqc = True
totalFragments = True
fast = False
runLocal = False
submit = True
pars = {'pipeline':pipeline,'threads':numThreads, 'alignerIndex':alignerIndex, 'end':end, 'records':records1, 'stranded':stranded, 'gtf':gtf, 'fastqc':fastqc, 'fast':fast, 'reference':reference, 'totalFragments':totalFragments, 'known1':known1, 'known2':known2, 'bed':bed}

for sampleReplicate in keys2:

    # create a script to be executed from job array
    script = '/'.join([pipeline,'scripts',sampleReplicate + '.sh']) 
    with open(script,'w') as out1:
        # update pars dictionary
        pars['sampleReplicate'] = sampleReplicate
        pars['out'] = out1

        # write yo header
        pars['out'].write('#!/bin/bash\n')

        # *** check to make sure sample has not already been successfully run ***
#        pars['flavor'] = 'standard'
#        check.isCompleted(pars)

        # *** 02 preprocess ***
        pars['flavor'] = 'standard'
#        pars['flavor'] = 'skip'
        pp.preprocess(pars)

        # *** 03 align *** 
        pars['flavor'] = 'bwa'
#        pars['flavor'] = 'skip' 
        a.align(pars) 

        # *** 04 combine ***
        pars['flavor'] = 'merge'
#        pars['flavor'] = 'skip'
        c.combine(pars)

        # *** 05 postprocess ***
        pars['flavor'] = 'gatk'
#        pars['flavor'] = 'skip'
        pop.postprocess(pars)

        # *** 06 qc ***
        pars['flavor'] = 'standard'
#        pars['flavor'] = 'skip'
        qc.qc(pars)

        # *** 20 clean *** 
        pars['flavor'] = 'sequencingCore'
#        cl.clean(pars) 

    # update permissions
    cmd = 'chmod 755 ' + script
    subprocess.check_call(cmd,shell=True) 

# execute script
if runLocal:
    print script
    subprocess.check_call(script,shell=True)
else:
    cmd = 'qsub -o ' + pipeline + '/logs -N ' + pipeline + ' ' + pbs
    print cmd

    if submit:
        subprocess.check_call(cmd,shell=True)
