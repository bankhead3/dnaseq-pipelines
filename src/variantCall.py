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
        outDir = pars['pipeline'] + '/01-mutect2/' + sampleReplicate + '/'
        outDir_base = pars['pipeline'] + '/01-mutect2/'
        subprocess.check_call('mkdir -p ' + outDir, shell=True)
        pars['vcf'] = outDir + pars['uName'] + '.vcf' 

        # call mutect
        tumorBam = pars['record']['tumorBam']
        interval = pars['record']['interval']
        cmd = 'time java -jar /sw/med/centos7/gatk/3.6/GenomeAnalysisTK.jar -T MuTect2 -L ' + interval + ' -I:tumor ' + tumorBam + ' -R ' + pars['reference'] + ' -o ' + pars['vcf']
        pars['out'].write(cmd + '\n\n')
    # mutect2 tumor only variant calling
    if pars['flavor'] == 'mutect2-tn':

        # create target directory
        outDir = pars['pipeline'] + '/02-mutect2/' + sampleReplicate + '/'
        outDir_base = pars['pipeline'] + '/02-mutect2/'
        subprocess.check_call('mkdir -p ' + outDir, shell=True)
        pars['vcf'] = outDir + pars['uName'] + '.vcf' 

        # call mutect
        tumorBam = pars['record']['tumorBam']
        normalBam = pars['record']['normalBam']
        interval = pars['record']['interval']
        cmd = 'time java -jar /sw/med/centos7/gatk/3.6/GenomeAnalysisTK.jar -T MuTect2 -L ' + interval + ' -I:tumor ' + tumorBam + ' -I:normal ' + normalBam + ' -R ' + pars['reference'] + ' -o ' + pars['vcf']
        pars['out'].write(cmd + '\n\n')
    # muse
    elif pars['flavor'] == 'muse':

        # create target directory
        outDir = pars['pipeline'] + '/03-muse/' + sampleReplicate + '/'
        outDir_base = pars['pipeline'] + '/03-muse/'
        subprocess.check_call('mkdir -p ' + outDir, shell=True)
        pars['prefix'] = outDir + pars['uName']

        # call mutect
        tumorBam = pars['record']['tumorBam']
        normalBam = pars['record']['normalBam']
        interval = pars['record']['interval']
        cmd = '# time /home/bankhead/bt/software/MuSE/1.0rc/MuSEv1.0rc_submission_b391201 call -O ' + pars['prefix'] + ' -f ' + pars['reference'] + ' -r ' + interval + ' ' + tumorBam + ' ' + normalBam
        pars['out'].write(cmd + '\n')
        cmd = 'time /home/bankhead/bt/software/MuSE/1.0rc/MuSEv1.0rc_submission_b391201 call -O ' + pars['prefix'] + ' -f ' + pars['reference'] + ' -r ' + interval + ' ' + tumorBam + ' ' + normalBam
        pars['out'].write(cmd + '\n\n')
    elif pars['flavor'] == 'skip':
        pass
    else:
        print pars['flavor']
        raise 'DONT UNDERSANT POST PROCESS FLAVOR!'

    mu.logTime(pars['out'],'FINISH VARIANT CALL')
