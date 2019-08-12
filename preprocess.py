#!/usr/bin/python

import sys
sys.path.append('utils')
import myUtils as mu

import subprocess

# 02 preprocess
def preprocess(pars):
    mu.logTime(pars['out'],'START PREPROCESS')

    records = pars['records']
    files = sorted([records[key]['file'] for key in records.keys() if records[key]['sampleReplicate'] == pars['sampleReplicate']])

    subprocess.check_call('mkdir -p ' + pars['pipeline'] + '/02-reads',shell=True)
    subprocess.check_call('mkdir -p ' + pars['pipeline'] + '/02-reads/fastq',shell=True)
    subprocess.check_call('mkdir -p ' + pars['pipeline'] + '/02-reads/ubam',shell=True)
    if pars['fastqc']:
        subprocess.check_call('mkdir -p ' + pars['pipeline'] + '/02-reads/fastqc',shell=True)
    if pars['totalFragments']:
        subprocess.check_call('mkdir -p ' + pars['pipeline'] + '/02-reads/totalFragments',shell=True)
        
    # get uniquenames and set up dictionary to contain associated files
    pars['uniqueNames'] = sorted(set(list([records[key]['uniqueName'] for key in records.keys() if records[key]['sampleReplicate'] == pars['sampleReplicate']])))
    for uniqueName in pars['uniqueNames']:
        pars[uniqueName] = dict()
        pars[uniqueName]['fastq1'] = pars['pipeline'] + '/02-reads/fastq/' + uniqueName + '-R1.fastq'
        pars[uniqueName]['fastq2'] = pars['pipeline'] + '/02-reads/fastq/' + uniqueName + '-R2.fastq'
        pars[uniqueName]['ubam'] = pars['pipeline'] + '/02-reads/ubam/' + uniqueName + '.bam'

    pars['out'].write('echo preprocess \n')


    # generates fastq files for alignment, ubam for merging later, and total fragement counts
    if pars['flavor'] == 'standard':
        # need to get pairs of files that are associated with a given coreSampleLabel
        for uniqueName in pars['uniqueNames']:

            myFiles = sorted([records[key]['file'] for key in records.keys() if records[key]['uniqueName'] == uniqueName])
            assert len(myFiles) <= 2, 'SHOULD ONLY BE NO MORE THAN 2 MYFILES ASSOCIATED...'

            # process first fastq file
            in1 = myFiles[0]

            # *** copy over reads as is (unless fast) ***
            tmp = ' > ' if not pars['fast'] else ' | head -n 400000 > '
            pars['out'].write('zcat ' + in1 + tmp + pars[uniqueName]['fastq1'] + '\n')                    
            if pars['fastqc']:
                pars['out'].write('fastqc ' + pars[uniqueName]['fastq1'] + ' --outdir=' + pars['pipeline'] + '/02-reads/fastqc/' + '\n')

            # for paired end data we have two sets of fasteq reads per uniqueName
            if pars['end'] == 'paired':
                in2 = myFiles[1] if pars['end'] == 'paired' else none

                tmp = ' > ' if not pars['fast'] else ' | head -n 400000 > '
                pars['out'].write('zcat ' + in2 + tmp + pars[uniqueName]['fastq2'] + '\n')                    
                if pars['fastqc']:
                    pars['out'].write('fastqc ' + pars[uniqueName]['fastq2'] + ' --outdir=' + pars['pipeline'] + '/02-reads/fastqc/' + '\n')

            # convert to ubam
            readGroup = uniqueName
            cmd = 'time java -jar /sw/med/centos7/picard/2.4.1/picard.jar FastqToSam FASTQ=' + pars[uniqueName]['fastq1'] + ' FASTQ2=' + pars[uniqueName]['fastq2'] + ' O=' + pars[uniqueName]['ubam'] + ' READ_GROUP_NAME=' + uniqueName + ' SAMPLE_NAME=' + pars['sampleReplicate'] + ' PLATFORM=illumina ' + ' \n'
            pars['out'].write(cmd)
            pars['out'].write('\n')

    # assumes ubams have been generated - gathers names
    elif pars['flavor'] == 'skip':

        pass

    # dont understand
    else:
        print pars['flavor']
        raise 'DONT UNDERSTAND PREPROCESS FLAVOR!!'

    # get total fragments per uniqueName
    if pars['totalFragments']:
        for uniqueName in pars['uniqueNames']:
            # get raw file
            myFiles = sorted([records[key]['file'] for key in records.keys() if records[key]['uniqueName'] == uniqueName])
            assert len(myFiles) <= 2, 'SHOULD ONLY BE NO MORE THAN 2 MYFILES ASSOCIATED...'
            rawFile = myFiles[0]

            # get processed file
            processedFile = pars[uniqueName]['fastq1']
            
            # count reads
            rawReadCountFile = pars['pipeline'] + '/02-reads/totalFragments/raw-' + uniqueName + '.txt'
            readCountFile = pars['pipeline'] + '/02-reads/totalFragments/' + uniqueName + '.txt'
            pars['out'].write("wc -l " + rawFile + "| awk '{print $1/4}' > " + rawReadCountFile + '\n')
            pars['out'].write("wc -l " + processedFile + "| awk '{print $1/4}' > " + readCountFile + '\n')

    mu.logTime(pars['out'],'FINISH PREPROCESS')
