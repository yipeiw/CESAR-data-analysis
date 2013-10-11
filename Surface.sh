#!/bin/bash

root=/home/yipeiw/Documents/Research-2013fall

tool=$root/LabelAnalysis/surfaceAnalysis.py

dataPath=$root/CESAR_data/annotated
outPath=$root/LabelAnalysis/result

for sub in $dataPath/*;
do
	sub=$(basename $sub)
	objectfile=$dataPath/$sub/object-reference.xml
	outputPath=$outPath/$sub
	mkdir -p $outputPath
	echo "$tool $objectfile $outputPath"
	$tool $objectfile $outputPath
done
