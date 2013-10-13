#!/bin/bash

root=/home/yipeiw/Documents

tool=$root/analysis/CESAR-data-analysis/surfaceAnalysis.py

dataPath=$root/data/CESAR
outPath=$root/analysis/CESAR-data-analysis/result

for sub in $dataPath/*;
do
	sub=$(basename $sub)
	objectfile=$dataPath/$sub/object-reference.xml
	outputPath=$outPath/$sub
	mkdir -p $outputPath
	echo "$tool $objectfile $outputPath"
	$tool $objectfile $outputPath
done
