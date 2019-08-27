#!/bin/bash
# when pulling from tcga add -n to ln params


# link to unpivoted expression file
inFile1=../../01--build-fastq-catalog/output/fastqCatalog20190816.txt
outFile1=input/fastqCatalog.txt
cmd="ln -sf $inFile1 $outFile1"
echo $cmd; eval $cmd


