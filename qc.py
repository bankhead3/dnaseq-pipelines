#!/usr/bin/python
# run qorts for post alignment qc

import sys
sys.path.append('utils')
import myUtils as mu

import subprocess

def qc(pars):
    mu.logTime(pars['out'],'START QC')

    sampleReplicate = pars['sampleReplicate']
    bam = pars[sampleReplicate]['bam4']
    outDir = pars['pipeline'] + '/06-qc/' + sampleReplicate + '/'
    outDir_base = pars['pipeline'] + '/06-qc/'
    subprocess.check_call('mkdir -p ' + outDir, shell=True)
    
    if pars['flavor'] == 'standard':
        pars[sampleReplicate]['depth'] = outDir + 'depth.txt'
        pars[sampleReplicate]['stats'] = outDir + 'stats.txt'

        # generate depth for coveraged regions
        cmd = 'samtools depth -b ' + pars['bed'] + ' ' + pars[sampleReplicate]['bam4'] + ' > ' + pars[sampleReplicate]['depth'] 
        pars['out'].write(cmd + '\n\n')

        # generate stats
        cmd = 'samtools stats ' + pars[sampleReplicate]['bam4'] + ' > ' + pars[sampleReplicate]['stats'] 
        pars['out'].write(cmd + '\n\n')

        # assemble parameters

    mu.logTime(pars['out'],'FINISH QC')
