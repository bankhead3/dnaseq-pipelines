#!/bin/bash

myDate=$(date +%Y%m%d)
mkdir -p intermediate
mkdir -p figs
mkdir -p output
mkdir -p input

if [ 1 == 1 ]; then 

# create two files one sample metadata and the other with chip expression
cmd="./01-pull-data.sh"
echo $cmd; eval $cmd

# gather fq files and sample names
cmd="./02-build-fq2sample.sh"
echo $cmd; eval $cmd
utils/qc.sh intermediate/02.txt 1

fi

# map unique names to samples and replicates
cmd="./03-map-to-samples.py"
echo $cmd; eval $cmd
utils/qc.sh intermediate/02.txt 1

# pivot to catalog
cmd="./04-pivot.py"
echo $cmd; eval $cmd
utils/qc.sh intermediate/04.txt 1-3

cmd="cp intermediate/04.txt output/fastqCatalog$myDate.txt"
echo $cmd; eval $cmd
