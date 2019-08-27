#!/bin/bash
# builds sampleFiles file

inFile1=intermediate/fastq-catalog.txt
outFile1=intermediate/sample-replicate-catalog.txt
head -n1 $inFile1 | cut -f3 > $outFile1
tail -n+2 $inFile1 | cut -f3 | sort | uniq >> $outFile1

inFile1=intermediate/fastq-catalog.txt
outFile1=intermediate/sample-replicate-catalog-1.txt
head -n1 $inFile1 | cut -f3 > $outFile1
tail -n+2 $inFile1 | cut -f3 | sort | uniq | head -n1 >> $outFile1

inFile1=intermediate/fastq-catalog.txt
outFile1=intermediate/sample-replicate-catalog-3.txt
head -n1 $inFile1 | cut -f3 > $outFile1
tail -n+2 $inFile1 | cut -f3 | sort | uniq | head -n3 >> $outFile1
