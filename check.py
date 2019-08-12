#!/usr/bin/python
# check if files are present and if they are then kick out of the script

import sys
sys.path.append('utils')
import myUtils as mu

import os

# clean
def isCompleted(pars):
    mu.logTime(pars['out'],'START COMPLETION CHECK')

    if pars['flavor'] == 'cufflinks':
        file = pars['pipeline'] + '/05-quantified/' + pars['sampleReplicate'] + '-genes.fpkm'
    elif pars['flavor'] == 'qorts':
        file = pars['pipeline'] + '/10-qc/' + pars['sampleReplicate'] + '/QC.summary.txt'
    elif pars['flavor'] == 'salmon' or pars['flavor'] == 'salmon-bias' or pars['flavor'] == 'salmon-bias-stranded':
        file = pars['pipeline'] + '/05-quantified/' + pars['sampleReplicate'] + '-abundance.txt'

    pars['out'].write('echo "checking if ' + file + ' exists..."' + '\n')
    pars['out'].write('if [ -e ' + file + ' ]; then ' + '\n')
    pars['out'].write('  echo "already processed ' + pars['sampleReplicate'] + '...exiting..." ' + '\n')
    pars['out'].write('  exit ' + '\n')
    pars['out'].write('else ' + '\n')
    pars['out'].write('  echo "not found...processing..."' + '\n')
    pars['out'].write('fi ' + '\n')



    mu.logTime(pars['out'],'FINISH COMPLETION CHECK')
