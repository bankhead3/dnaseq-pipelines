#!/bin/bash
# builds sampleFiles file


inFile1=input/params.txt
localDir=input/run/
globalDir=$(grep globalPath $inFile1 | cut -f2)

lane=1

files=$(find -L $localDir -name '*q.gz' | sort | grep -v Undetermined)
outFile=intermediate/02.txt

# make paths sed compatible
localDir=$(echo $localDir | sed 's_/_\\/_g')
globalDir=$(echo $globalDir | sed 's_/_\\/_g')

echo -e "file\tsampleID\tread\tlane" > $outFile
for file in $files
do

  global=$(echo $file | sed "s/$localDir/$globalDir/")
  sampleID=$(basename $file | sed 's/_USE.*//' | sed 's/._//' | sed 's/WT//')

  grep '_1.*q.gz' <(echo $file) > /dev/null
  if [ $? -eq 0 ]; then
    read=1
  else
    read=2
  fi

  echo -e "$global\t$sampleID\t$read\t$lane" >> $outFile
done
