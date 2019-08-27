#!/bin/bash

myDate=$(date +%Y%m%d)
mkdir -p intermediate
mkdir -p figs
mkdir -p output
mkdir -p input

if [ 0 == 1 ]; then

# create two files one sample metadata and the other with chip expression
cmd="./01-pull-data.sh"
echo $cmd; eval $cmd
exit
cmd="./02-build-fastq-catalog.py"
echo $cmd; eval $cmd
../utils/qc.sh intermediate/fastq-catalog.txt 1

cmd="./05-gather-counts.sh"
echo $cmd; eval $cmd
../utils/qc.sh intermediate/05.txt 1-2

cmd="./06-pivot-counts.py"
echo $cmd; eval $cmd
../utils/qc.sh intermediate/06.txt 1

cmd="cp intermediate/06.txt output/fragmentCounts$myDate.txt"
echo $cmd; eval $cmd
fi

cmd="./06-build-vc-catalogs.py"
echo $cmd; eval $cmd
../utils/qc.sh intermediate/vc-catalog.txt 1,5


exit

cmd="./15-gather-annovar.py"
echo $cmd; eval $cmd
../utils/qc.sh intermediate/15.txt 1-12

cmd="./16-gather-annovar.py"
echo $cmd; eval $cmd
../utils/qc.sh intermediate/16.txt 1-7

cmd="./17-parse-vcf.py"
echo $cmd; eval $cmd
../utils/qc.sh intermediate/17.txt 1-6

cmd="./18-combine.py"
echo $cmd; eval $cmd
../utils/qc.sh intermediate/18.txt 1-15
fi
cmd="Rscript 19-summarize.R > intermediate/19.rout"
echo $cmd; eval $cmd
../utils/qc.sh intermediate/19.txt 1,2

cmd="Rscript 20-filter.R > intermediate/20.rout"
echo $cmd; eval $cmd
../utils/qc.sh intermediate/20.txt 1-15

cmd="cp intermediate/18.txt output/allVariantDetails$myDate.txt"
echo $cmd; eval $cmd
cmd="cp intermediate/20.txt output/variantDetails$myDate.txt; ../utils/txt2excel.py output/variantDetails$myDate.txt"
echo $cmd; eval $cmd
cmd="cp intermediate/19.txt output/geneVariantCounts$myDate.txt"
echo $cmd; eval $cmd
