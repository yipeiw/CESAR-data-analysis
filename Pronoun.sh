#!/bin/bash

root=/home/yipeiw/Documents

tool=$root/Research-2013fall/LabelAnalysis/pronounAnalysis.py

dataPath=$root/Research-2013fall/LabelAnalysis/result

for sub in $dataPath/*;
do
	surfacefile=$sub/surfaceLayer.txt
	outputfile=$sub/pronountest.txt
	echo "$tool $surfacefile $outputfile"
	$tool $surfacefile $outputfile
done
