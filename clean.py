#!/usr/bin/python
# delete files you don't need anymore

import sys
sys.path.append('utils')
import myUtils as mu

# clean
#def clean(step,sampleReplicate,pipeline,out):
def clean(pars):
    mu.logTime(pars['out'],'START CLEAN')

    if pars['flavor'] == 'sequencingCore':
        mu.writeCmd(pars['out'], 'rm -f ' + pars['pipeline'] + '/02-reads/fastq/*' + pars['sampleReplicate'] + '*.fastq')
        mu.writeCmd(pars['out'], 'rm -f ' + pars['pipeline'] + '/02-reads/ubam/*' + pars['sampleReplicate'] + '*.bam')
        mu.writeCmd(pars['out'], 'rm -f ' + pars['pipeline'] + '/03-combined/fastq/' + pars['sampleReplicate'] + '*.fastq')

    mu.logTime(pars['out'],'FINISH CLEAN')
