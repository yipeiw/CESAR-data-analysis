#!/bin/bash

root=/home/yipeiw/Documents/Research-2013fall

tool=$root/LabelAnalysis/NDUcorrelation.py

OPath=$root/LabelAnalysis/result
dataPath=$root/CESAR_data/annotated
outPath=$root/LabelAnalysis/result

for sub in $dataPath/*;
do
	sub=$(basename $sub)
	objectfile=$OPath/$sub/surfaceLayer.txt
	NDUfile=$dataPath/$sub/NDU.xml
	outputPath=$outPath/$sub
	mkdir -p $outputPath
	echo "$tool $objectfile $outputPath"
	$tool $NDUfile $objectfile $outputPath
done
