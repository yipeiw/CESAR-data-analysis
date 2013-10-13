#!/bin/bash

root=/home/yipeiw/Documents

tool=$root/analysis/CESAR-data-analysis/pronounAnalysis.py

dataPath=$root/analysis/CESAR-data-analysis/result

for sub in $dataPath/*;
do
	surfacefile=$sub/surfaceLayer.txt
	outputfile=$sub/pronoun.txt
	echo "$tool $surfacefile $outputfile"
	$tool $surfacefile $outputfile
done
