#!/usr/bin/python
# reformats fastq catalog 

import sys
sys.path.append('../utils')
import myUtils as mu

import re

inFile1 = 'input/fastqCatalog.txt'
outFile1 = 'intermediate/fastq-catalog.txt'

(records1,header1,keys1) = mu.readRecords(inFile1,['sampleReplicate','lane'])

# write yo out
with open(outFile1,'w') as out1:

    # write yo header
    header = ['file','uniqueName','sampleReplicate','read']
    out1.write('\t'.join(header) + '\n')

    # for each barcode write 2 lines
    for myKey in keys1:
        record = records1[myKey]

        sampleReplicate,lane = record['sampleReplicate'],record['lane']
        uniqueName = myKey.replace('!','__')

        file1,file2 = record['fastq.gz1'],record['fastq.gz2'],

        # assemble and write line out
        lineOut1 = [file1,uniqueName,sampleReplicate,'1']
        lineOut2 = [file2,uniqueName,sampleReplicate,'2']
        out1.write('\t'.join(lineOut1) + '\n')
        out1.write('\t'.join(lineOut2) + '\n')
