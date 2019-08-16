#!/usr/bin/python
# pivot up sample fastq file catalog

import sys
sys.path.append('utils')
import myUtils as mu

import re

inFile1 = 'intermediate/03.txt'
outFile1 = 'intermediate/04.txt'

(records1,header1,keys1) = mu.readRecords(inFile1,['file'])

sampleReplicateLanes = sorted(list(set(['-'.join([records1[key]['sampleReplicate'],records1[key]['lane']]) for key in keys1])))

# write yo output file
with open(outFile1,'w') as out1:
    
    # write yo header
    header = ['sampleReplicate','lane','cellline','tx', 'replicate', 'fastq.gz1','fastq.gz2']
    out1.write('\t'.join(header) + '\n')

    for sampleReplicateLane in sampleReplicateLanes:
        parse1 = sampleReplicateLane.split('-')
        assert len(parse1) == 4, 'CANT PARSE RUNLANESAMPLEREPLICATE'
        cellLine,treatment,replicate,lane = parse1
        sampleReplicate = '-'.join([cellLine,treatment,replicate])


        files = sorted([records1[key]['file'] for key in keys1 if records1[key]['sampleReplicate'] == sampleReplicate])
        print sampleReplicate
        assert len(files) == 2, 'NOT 2 FASTQ FILES'
        file1,file2 = files[0],files[1]

        # assemble and write line out
        lineOut = [sampleReplicate,lane,cellLine,treatment,replicate,file1,file2]
        out1.write('\t'.join(lineOut) + '\n')
