#!/bin/bash

root=/home/yipeiw/Documents

tool=$root/Research-2013fall/LabelAnalysis/OB_context.py
dataPath=$root/Research-2013fall/CESAR_data/annotated

outputPath=$root/Research-2013fall/LabelAnalysis/context
mkdir -p $outputPath

for sub in $dataPath/*;
do
	sub=$(basename $sub)
	objectfile=$dataPath/$sub/object-reference.xml
	outputfile=$outputPath/$sub.txt
	echo "$tool $objectfile $outputfile"
	$tool $objectfile $outputfile
done
