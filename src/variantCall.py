#!/usr/bin/python

import sys
sys.path.append('utils')
import myUtils as mu

import subprocess

# 02 preprocess
def vc(pars):
    mu.logTime(pars['out'],'START VARIANT CALL')

    sampleReplicate = pars['sampleReplicate']

    # mutect2 tumor only variant calling
    if pars['flavor'] == 'mutect2-t':

        # create target directory
        outDir = pars['pipeline'] + '/01-variants/' + sampleReplicate + '/'
        outDir_base = pars['pipeline'] + '/01-variants/'
        subprocess.check_call('mkdir -p ' + outDir, shell=True)
        pars['vcf'] = outDir + pars['uName'] + '.vcf' 

        # call mutect
        tumorBam = pars['record']['tumorBam']
        interval = pars['record']['interval']
        cmd = 'time java -jar /sw/med/centos7/gatk/3.6.1/GenomeAnalysisTK.jar -T MuTect2 -L ' + interval + ' -I:tumor ' + tumorBam + ' -R ' + pars['reference'] + ' -o ' + pars['vcf']
        pars['out'].write(cmd + '\n\n')
    # mutect2 tumor only variant calling
    if pars['flavor'] == 'mutect2-tn':

        # create target directory
        outDir = pars['pipeline'] + '/02-variants/' + sampleReplicate + '/'
        outDir_base = pars['pipeline'] + '/02-variants/'
        subprocess.check_call('mkdir -p ' + outDir, shell=True)
        pars['vcf'] = outDir + pars['uName'] + '.vcf' 

        # call mutect
        tumorBam = pars['record']['tumorBam']
        normalBam = pars['record']['normalBam']
        interval = pars['record']['interval']
        cmd = 'time java -jar /sw/med/centos7/gatk/3.6.1/GenomeAnalysisTK.jar -T MuTect2 -L ' + interval + ' -I:tumor ' + tumorBam + ' -I:normal ' + normalBam + ' -R ' + pars['reference'] + ' -o ' + pars['vcf']
        pars['out'].write(cmd + '\n\n')
    elif pars['flavor'] == 'skip':
        pass
    else:
        print pars['flavor']
        raise 'DONT UNDERSANT POST PROCESS FLAVOR!'

    mu.logTime(pars['out'],'FINISH VARIANT CALL')
