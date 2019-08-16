#!/bin/bash
# when pulling from tcga add -n to ln params


# link to directory containing gdc bam directories
inFile1=/home/bankhead/bt/rawData/neamati/yibinNovogene20190725/C202SC19060654/raw_data
outFile1=input/run
cmd="ln -sfn $inFile1 $outFile1"
echo $cmd; eval $cmd



