#!/usr/bin/python
# unknown flavors will be ignored

import sys
sys.path.append('utils')
import myUtils as mu

import subprocess

# align
#def align(flavor,out,records,sampleLabel,pipeline,fastqFiles,numThreads,alignerIndexDir):
def align(pars):
    mu.logTime(pars['out'],'START ALIGN')

    inDir = pars['pipeline'] + '/02-reads/ubam/'
    outDir = pars['pipeline'] + '/03-aligned/'

    subprocess.check_call('mkdir -p ' + outDir, shell=True)
    if pars['totalFragments']:
        subprocess.check_call('mkdir -p ' + outDir + 'totalFragments/',shell=True)
    pars['out'].write('echo align \n')

    for uniqueName in pars['uniqueNames']:
        pars[uniqueName]['bam1'] = outDir + uniqueName + '.bam'

    # *** bwa ***
    if pars['flavor'] == 'bwa':

        for uniqueName in pars['uniqueNames']:

            # call bwa and generate bam
            cmd = 'bwa mem -v 1 -t ' + pars['threads'] + ' -Y ' + pars['alignerIndex'] + ' ' + pars[uniqueName]['fastq1'] + ' ' + pars[uniqueName]['fastq2'] + ' | samtools sort -n -@' + pars['threads'] + ' -o ' + pars[uniqueName]['bam1'] + ' - \n'
#            cmd = 'bwa mem -v 1 -t ' + pars['threads'] + ' -Y ' + pars['alignerIndex'] + ' ' + pars[uniqueName]['fastq1'] + ' ' + pars[uniqueName]['fastq2'] + ' | samtools view -b > ' + pars[uniqueName]['bam1'] + ' \n'
            pars['out'].write('# ' + cmd)
            pars['out'].write(cmd)
#            pars['out'].write('samtools index ' + pars[uniqueName]['bam1'] + ' \n')

            # *** remove fastq files here ***
            pars['out'].write('\n')

    elif pars['flavor'] == 'skip':
        pass
    else:
        print pars['flavor']
        raise 'DONT UNDERSTAND FLAVOR!!!'

    # get total fragments per uniqueName
    if pars['totalFragments']:
        for uniqueName in pars['uniqueNames']:
            countFile = outDir + 'totalFragments/' + uniqueName + '.txt'
            tmp1 = outDir + uniqueName + '.tmp1.txt'
            tmp2 = outDir + uniqueName + '.tmp2.txt'
            pars['out'].write('samtools view -F 4 ' + pars[uniqueName]['bam1'] + ' | cut -f1 > ' + tmp1 + '\n')
            pars['out'].write('sort ' + tmp1 + ' | uniq > ' + tmp2 + '\n')
            pars['out'].write('wc -l ' + tmp2 + ' | sed "s/ .*//" > ' + countFile + '\n')
            pars['out'].write('rm -f ' + tmp1 + ' ' + tmp2 + '\n')

    mu.logTime(pars['out'],'FINISH ALIGN')
