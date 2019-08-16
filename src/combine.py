#!/usr/bin/python

import sys
sys.path.append('utils')
import myUtils as mu

import subprocess

# 03 combine
def combine(pars):
    mu.logTime(pars['out'],'START COMBINE')

    outDir = pars['pipeline'] + '/04-combined/'
    subprocess.check_call('mkdir -p ' + outDir, shell=True)
    if pars['totalFragments']:
        subprocess.check_call('mkdir -p ' + outDir + 'totalFragments/',shell=True)

    # set up variables for bam locations
    for uniqueName in pars['uniqueNames']:
        pars[uniqueName]['bam2'] = outDir + uniqueName + '.bam'
    pars[pars['sampleReplicate']] = dict()
    pars[pars['sampleReplicate']]['bam1'] = outDir + pars['sampleReplicate'] + '.bam'    

    if pars['flavor'] == 'merge':
        
        # merge ubam with aligned bam for each unique name
        for uniqueName in pars['uniqueNames']:
            # merge bam here
            cmd = 'time java -jar /sw/med/centos7/picard/2.4.1/picard.jar MergeBamAlignment ALIGNED=' + pars[uniqueName]['bam1'] + ' UNMAPPED=' + pars[uniqueName]['ubam'] + ' O=' + pars[uniqueName]['bam2'] + ' R=' + pars['reference']
            pars['out'].write(cmd + '\n')
            pars['out'].write('\n')

        # merge separate uniqueName bams into a single sampleReplicate bam
        tmp = ''
        for uniqueName in pars['uniqueNames']:
            tmp += 'I=' + pars[uniqueName]['bam2'] + ' '
        cmd = 'time java -jar /sw/med/centos7/picard/2.4.1/picard.jar MergeSamFiles ' + tmp + ' O=' + pars[pars['sampleReplicate']]['bam1'] + ' SORT_ORDER=coordinate CREATE_INDEX=true'
        pars['out'].write(cmd + '\n')
        pars['out'].write('\n')

        # remove unique sample bams
        for uniqueName in pars['uniqueNames']:
            pars['out'].write('rm -f ' + pars[uniqueName]['bam2'] + '\n')

    elif pars['flavor'] == 'skip':
        pass
    else:
        print pars['flavor']
        raise 'DO NOT UNDERSTAND COMBINE FLAVOR!!'

    # get total fragments per uniqueName
    if pars['totalFragments']:
        """
        for uniqueName in pars['uniqueNames']:
            countFile = outDir + 'totalFragments/' + uniqueName + '.txt'
            tmp1 = outDir + uniqueName + '.tmp1.txt'
            tmp2 = outDir + uniqueName + '.tmp2.txt'
            pars['out'].write('samtools view -F 4 ' + pars[uniqueName]['bam1'] + ' | cut -f1 > ' + tmp1 + '\n')
            pars['out'].write('sort ' + tmp1 + ' | uniq > ' + tmp2 + '\n')
            pars['out'].write('wc -l ' + tmp2 + ' | sed "s/ .*//" > ' + countFile + '\n')
            pars['out'].write('rm -f ' + tmp1 + ' ' + tmp2 + '\n')
        """

        sampleReplicate= pars['sampleReplicate']
        countFile = outDir + 'totalFragments/' + sampleReplicate + '.txt'
        tmp1 = outDir + sampleReplicate + '.tmp1.txt'
        tmp2 = outDir + sampleReplicate + '.tmp2.txt'
        pars['out'].write('samtools view -F 4 ' + pars[sampleReplicate]['bam1'] + ' | cut -f1 > ' + tmp1 + '\n')
        pars['out'].write('sort ' + tmp1 + ' | uniq > ' + tmp2 + '\n')
        pars['out'].write('wc -l ' + tmp2 + ' | sed "s/ .*//" > ' + countFile + '\n')
        pars['out'].write('rm -f ' + tmp1 + ' ' + tmp2 + '\n')
        pars['out'].write('\n')

    mu.logTime(pars['out'],'FINISH COMBINE')
    return
