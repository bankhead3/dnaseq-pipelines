#!/usr/bin/python

import sys
sys.path.append('../utils/')
import myUtils as mu

inFile1 = 'input/variant-calling-catalog.txt'
inFile2 = 'input/GRCh38.primary_assembly.genome.fa.chrom.sizes'
outFile1 = 'intermediate/vc-catalog.txt'

bamDir = 'pipeline1/05-polished/'

(records1,header1,keys1) = mu.readRecords(inFile1,['sampleReplicate','normal','variantCaller'])

# read chrom sizes
chromDict = dict()
with open(inFile2) as in1:
    for line in in1:
        parse1 = line.strip().split('\t')
        if 'chr' in parse1[0]:
            chromDict[parse1[0]] = dict()
            chromDict[parse1[0]]['size'] = int(parse1[1])
chroms = sorted(chromDict.keys())
# chroms = ['chr21']   # FOR TESTING

# construct intervals
num = 10
for chrom in chroms:
    size = chromDict[chrom]['size']
    intervalSize = size/num + 1

    # construct intervals
    iBegin = 1
    for interval in range(1,num+1):
        iEnd = intervalSize*interval if intervalSize*interval <= size else size
        chromDict[chrom][interval] = [iBegin,iEnd]
        iBegin = iEnd + 1

def writeLine(out,key,chroms):
        tumor,normal,caller = key.split('!')

        tumorBam = bamDir + tumor + '.bam'
        normalBam = 'NA' if normal == 'NA' else bamDir + normal + '.bam'

        # write you results
        for chrom in chroms:

            # only need one interval for chrM
            if chrom == 'chrM' or caller == 'muse':
                intervalLabel = chrom + '.1'
                interval = chrom
                uName = '_'.join([tumor,normal,intervalLabel,caller])
                lineOut = [uName,tumor,normal,caller,intervalLabel,interval,tumorBam,normalBam]
                out.write('\t'.join(lineOut) + '\n')
            else:
                for intervalNum in range(1,num+1):
                    iBegin,iEnd = chromDict[chrom][intervalNum]
                    intervalLabel = chrom + '.' + str(intervalNum)
                    interval = chrom + ':' + str(iBegin) + '-' + str(iEnd)
                    uName = '_'.join([tumor,normal,intervalLabel,caller])
                    lineOut = [uName,tumor,normal,caller,str(intervalLabel),interval,tumorBam,normalBam]
                    out.write('\t'.join(lineOut) + '\n')

# read
header = ['uName','sampleReplicate','normal','caller','intervalNum','interval','tumorBam','normalBam']
with open(outFile1,'w') as out1:

    # write yo header
    out1.write('\t'.join(header) + '\n')

    # mutect2 tumor v normal
    keys1a = [key for key in keys1 if records1[key]['variantCaller'] == 'mutect2' and records1[key]['normal'] != 'NA']
    for key in keys1a:
        writeLine(out1,key,chroms)

    # muse tumor v normal
    keys1a = [key for key in keys1 if records1[key]['variantCaller'] == 'muse']
    for key in keys1a:
        writeLine(out1,key,chroms)
