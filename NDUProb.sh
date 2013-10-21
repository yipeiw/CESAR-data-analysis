#!/bin/bash

root=/home/yipeiw/Documents/Research-2013fall

tool=$root/LabelAnalysis/NDUEstimation.py

OPath=$root/LabelAnalysis/result
dataPath=$root/CESAR_data/annotated
outputPath=$root/LabelAnalysis/NDU_estimate
mkdir -p $outputPath

#for sub in $dataPath/*;
#do
	#sub=$(basename $sub)
sub=CESAR_Jun-Sun-3-09-09-17-2012
	objectfile=$OPath/$sub/surfaceLayer.txt
	NDUfile=$dataPath/$sub/NDU.xml
	echo "$tool $objectfile $outputPath"
	$tool $NDUfile $objectfile $outputPath
#done
