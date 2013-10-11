#!/usr/bin/env python

import os
import os.path as path

dataPath='/home/yipeiw/Documents/Research-2013fall/LabelAnalysis/result/'
outputfile='/home/yipeiw/Documents/Research-2013fall/LabelAnalysis/cleanResult/NDUcorrelation_merge.txt'

def LoadCorrelation(filepath):
	data={}
	for line in open(filepath):
		ndu, obNum, crossNum =line.strip().split(',')
		data[ndu]=[int(obNum), int(crossNum)]
	return data


filelist = [path.join(dataPath+subDir, 'NDU-reference.txt') for subDir in os.listdir(dataPath)]

Record={}

for ndufile in filelist:
	if not path.exists(ndufile):
		print "not exist ", ndufile
		continue

	nduDict = LoadCorrelation(ndufile)
	for ob, infos in nduDict.items():
		if ob in Record.keys():
			old = Record[ob]
			Record[ob] = [old[i]+infos[i] for i in range(0, len(infos))]+[old[len(old)-1]+1]
		else:
			Record[ob] = infos+[1]

fout = open(outputfile, 'w')
rankRecord=sorted(Record.items(), key=lambda item:(item[1][0], item[1][2]), reverse=True)
for ob, infos in rankRecord:
	fout.write("%s,%.3f,%.3f,%s\n" % (ob, float(infos[0])/infos[2], float(infos[1])/infos[2], infos[2]))

fout.close()	
