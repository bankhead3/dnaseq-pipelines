#!/usr/bin/python

import sys
sys.path.append('utils')
import myUtils as mu

import subprocess

# 02 preprocess
def postprocess(pars):
    mu.logTime(pars['out'],'START POSTPROCESS')

    sampleReplicate = pars['sampleReplicate']

    outDir = pars['pipeline'] + '/05-polished/' + sampleReplicate + '/'
    outDir_base = pars['pipeline'] + '/05-polished/'
    subprocess.check_call('mkdir -p ' + outDir, shell=True)
    if pars['totalFragments']:
        subprocess.check_call('mkdir -p ' + outDir + 'totalFragments/',shell=True)

    pars[sampleReplicate]['bam2'] = outDir + pars['sampleReplicate'] + '.df.bam'  # duplicates filtered
    pars[sampleReplicate]['dups'] = outDir + pars['sampleReplicate'] + '.df.txt'  # duplicates marked
    pars[sampleReplicate]['bam3'] = outDir + pars['sampleReplicate'] + '.bam'  # recalibrated 
    pars[sampleReplicate]['bam4'] = outDir_base + pars['sampleReplicate'] + '.bam'  # recalibrated in one directory up
    pars[sampleReplicate]['recal1'] = outDir + pars['sampleReplicate'] + '.recal1.txt'  # duplicates marked
    pars[sampleReplicate]['recal2'] = outDir + pars['sampleReplicate'] + '.recal2.txt'  # duplicates marked
    pars[sampleReplicate]['recal-plots'] = outDir + pars['sampleReplicate'] + '.recal-plots.pdf'  # duplicates marked

    if pars['flavor'] == 'gatk':
        # mark dups
        cmd = 'time java -jar /sw/med/centos7/picard/2.4.1/picard.jar MarkDuplicates REMOVE_DUPLICATES=true I=' + pars[sampleReplicate]['bam1'] + ' O=' + pars[sampleReplicate]['bam2'] + ' M=' + pars[sampleReplicate]['dups']
        pars['out'].write(cmd + '\n\n')

        # create index
        cmd = 'samtools index ' + pars[sampleReplicate]['bam2'] 
        pars['out'].write(cmd + '\n\n')

        # assess recalibrationt
        cmd = 'time java -jar /sw/med/centos7/gatk/3.6.1/GenomeAnalysisTK.jar -T BaseRecalibrator -I ' + pars[sampleReplicate]['bam2'] + ' -R ' + pars['reference'] + ' -knownSites ' + pars['known1'] + ' -knownSites ' + pars['known2'] + ' -o ' + pars[sampleReplicate]['recal1']
        pars['out'].write(cmd + '\n\n')

        # re-assess recalibration
        cmd = 'time java -jar /sw/med/centos7/gatk/3.6.1/GenomeAnalysisTK.jar -T BaseRecalibrator -I ' + pars[sampleReplicate]['bam2'] + ' -R ' + pars['reference'] + ' -knownSites ' + pars['known1'] + ' -knownSites ' + pars['known2'] + ' -BQSR ' + pars[sampleReplicate]['recal1'] + ' -o ' + pars[sampleReplicate]['recal2']
        pars['out'].write(cmd + '\n\n')

        # plot before and after
        cmd = 'time java -jar /sw/med/centos7/gatk/3.6.1/GenomeAnalysisTK.jar -T AnalyzeCovariates -R ' + pars['reference'] + ' -before ' + pars[sampleReplicate]['recal1'] + ' -after ' + pars[sampleReplicate]['recal2'] + ' -plots ' + pars[sampleReplicate]['recal-plots']
        pars['out'].write(cmd + '\n\n')

        # create a recalibrated bam
        cmd = 'time java -jar /sw/med/centos7/gatk/3.6.1/GenomeAnalysisTK.jar -T PrintReads -R ' + pars['reference'] + ' -I ' + pars[sampleReplicate]['bam2'] + ' -BQSR ' + pars[sampleReplicate]['recal1'] + ' -o ' + pars[sampleReplicate]['bam3']
        pars['out'].write(cmd + '\n\n')

        # move one directory up
        cmd = 'mv ' + pars[sampleReplicate]['bam3'] + ' ' + pars[sampleReplicate]['bam4']
        pars['out'].write(cmd + '\n\n')
        cmd = 'mv ' + pars[sampleReplicate]['bam3'].replace('.bam','.bai') + ' ' + pars[sampleReplicate]['bam4'].replace('.bam','.bai')
        pars['out'].write(cmd + '\n\n')

    elif pars['flavor'] == 'skip':
        pass
    else:
        print pars['flavor']
        raise 'DONT UNDERSANT POST PROCESS FLAVOR!'

    # get total fragments per uniqueName
    if pars['totalFragments']:
        countFile = outDir + 'totalFragments/' + sampleReplicate + '.df.txt'
        tmp1 = outDir + sampleReplicate + '.tmp1.txt'
        tmp2 = outDir + sampleReplicate + '.tmp2.txt'
        pars['out'].write('samtools view -F 4 ' + pars[sampleReplicate]['bam3'] + ' | cut -f1 > ' + tmp1 + '\n')
        pars['out'].write('sort ' + tmp1 + ' | uniq > ' + tmp2 + '\n')
        pars['out'].write('wc -l ' + tmp2 + ' | sed "s/ .*//" > ' + countFile + '\n')
        pars['out'].write('rm -f ' + tmp1 + ' ' + tmp2 + '\n')
        pars['out'].write('\n')

    mu.logTime(pars['out'],'FINISH POSTPROCESS')
