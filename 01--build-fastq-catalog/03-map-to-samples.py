#!/usr/bin/python
# read in run files from the core and map unique names to samples and replicates

import sys
sys.path.append('utils')
import myUtils as mu

import re

inFile1 = 'intermediate/02.txt'
inFile2 = 'input/params.txt'
outFile1 = 'intermediate/03.txt'

(records1,header1,keys1) = mu.readRecords(inFile1,['file'])
(records2,header2,keys2) = mu.readRecords(inFile2,['property'])

cellline = records2['cellline']['value']

# write yo file
with open(outFile1,'w') as out1:

    # write yo header
    header = header1 + ['sampleReplicate', 'cellline', 'tx', 'replicate']
    out1.write('\t'.join(header) + '\n')

    for myKey in keys1:
        record = records1[myKey]
        sampleID = record['sampleID']
        tx = sampleID[:-1]
        replicate = sampleID[-1]

        # update record
        record['sampleReplicate'] = '-'.join([cellline,tx,replicate])
        record['cellline'] = cellline
        record['tx'] = tx
        record['replicate'] = replicate

        # assemble and write line out
        lineOut = []
        for field in header:
            lineOut.append(record[field])
        out1.write('\t'.join(lineOut) + '\n')

        




