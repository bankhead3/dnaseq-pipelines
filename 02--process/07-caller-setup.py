#!/usr/bin/python
# this script sets up the directory structure, prefix.pbs, and execute.sh files
# customized for downloading lots of data from gdc data portal

import sys
sys.path.append('../utils')
sys.path.append('../utils/dnaseq-pipelines')

import myUtils as mu

import subprocess
import os
import re

inFile1 = 'intermediate/vc-catalog.txt'
pipeline = 'pipeline1-calls'

# combos 62 X 8 
# combos 124 X 4
nodes=50  # was 30
numThreads=str(4)  #12
pbsHeader = 'input/header-' + numThreads + '-array.pbs'

(na,na,keys1) = mu.readRecords(inFile1,['caller','sampleReplicate','interval'])
# keys1 = keys1[:3]

subprocess.check_call('mkdir -p ' + pipeline,shell=True)
subprocess.check_call('mkdir -p ' + '/'.join([pipeline,'logs']),shell=True)
subprocess.check_call('mkdir -p ' + '/'.join([pipeline,'scripts']),shell=True)

# create pbs prefix and execution script
pbs = '/'.join([pipeline,'prefix.pbs']) 
execute = pipeline + '/execute.sh'

# write pbs prefix
with open(pbs,'w') as out1, open(pbsHeader,'r') as in1:
    for line in in1:
        # copy prefix header except for array spec
        if '-t' in line:
            altLine = '#PBS -t 1-' + str(len(keys1)) + '%' + str(nodes) + '\n'
            out1.write(altLine)
        else:
            out1.write(line)
    out1.write(execute + ' $PBS_ARRAYID' + '\n')

# write execute script
with open(execute,'w') as out1:
    out1.write('#!/bin/bash' + '\n')
    out1.write('echo -e "PBS_ARRAYID\t$1"' + '\n')

    # assign variables based on array id
    out1.write('sampleReplicate=$(head -n$((1+$1)) ' + inFile1 + '| tail -n1 | cut -f1)' + '\n')

    # print sampleReplicate
    out1.write('echo -e "sampleReplicate\t$sampleReplicate"' + '\n')
    out1.write('echo' + '\n')

    mu.logTime(out1,'ALL START')

    # set up custom script 
    out1.write('cmd="./' + pipeline + '/scripts/$sampleReplicate.sh"' + '\n')
    out1.write('echo $cmd; eval $cmd' + '\n')

    mu.logTime(out1,'ALL FINISHED!')
    out1.write('echo' + '\n')

# update script permissions
cmd = 'chmod 755 ' + execute
subprocess.check_call(cmd,shell=True) 
