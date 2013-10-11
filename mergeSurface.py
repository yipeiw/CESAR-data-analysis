#!/usr/bin/env python

import os
import os.path as path

dataPath='/home/yipeiw/Documents/Research-2013fall/LabelAnalysis/result/'
outputfile='/home/yipeiw/Documents/Research-2013fall/LabelAnalysis/cleanResult/Surface_merge.txt'

def LoadSurface(surfacefile):
	data={}
	for line in open(surfacefile):
		ob, appearNum, expressNum, omitNum, driverA,driverE, driverO=line.strip().split(',')
		data[ob]=[int(appearNum), int(expressNum), int(omitNum), int(driverA), int(driverE), int(driverO)]
	return data


filelist = [path.join(dataPath+subDir, 'Surface.txt') for subDir in os.listdir(dataPath)]

Record={}

for surfacefile in filelist:
	if not path.exists(surfacefile):
		print "not exist ", surfacefile
		continue

	surfaceDict = LoadSurface(surfacefile)
	for ob, infos in surfaceDict.items():
		if ob in Record.keys():
			old = Record[ob]
			Record[ob] = [old[i]+infos[i] for i in range(0, len(infos))]+[old[len(old)-1]+1]
		else:
			Record[ob] = infos+[1]

fout = open(outputfile, 'w')
rankRecord=sorted(Record.items(), key=lambda item:(item[1][0], item[1][6]), reverse=True)
for ob, infos in rankRecord:
	fout.write("%s,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%s\n" % (ob, float(infos[0])/infos[6], float(infos[1])/infos[6], float(infos[2])/infos[6], float(infos[3])/infos[6], float(infos[4])/infos[6], float(infos[5])/infos[6], infos[6]))

fout.close()	
