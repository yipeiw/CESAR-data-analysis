#!/usr/bin/env python

import sys
sys.path.append('/home/yipeiw/Documents/Research-2013fall/Tool/AnnotationAnalysis')
import os.path as path
from read_write_annotation_files import *

from collections import defaultdict
import re

NDUfile=sys.argv[1]
objectfile=sys.argv[2]
outputPath=sys.argv[3]

def CheckCross(OBdict):
	rangeList = []
	for ob, boundary_list in OBdict.items():
		rankBoundary = sorted(boundary_list, key=lambda item:item[0])
		rangeList += [(ob, rankBoundary[0][0], rankBoundary[len(rankBoundary)-1][1])]

	overlap=defaultdict(bool)
	for i in range(0, len(rangeList)):
		ob, left, right = rangeList[i]
		for j in range(0, len(rangeList)):
			if j==i:
				continue
			ob_cmp, left_cmp, right_cmp = rangeList[j]
			if min(right, right_cmp)-max(left, left_cmp)>=0:
				overlap[ob]=True
				break	
	return len(overlap.keys())


def output(fout, ai, WordObjectDict, idxList):
	Used = defaultdict(bool)
	fout.write("<%s>\n" % (ai.name))
	for idx in sorted(idxList):
		obList = WordObjectDict[idx]
		for ob in obList:
			if not Used[ob]:
				fout.write("	%s,%s,%s,%s-%s,%s\n" % (ob[0], ob[1], ob[2], ob[4], ob[5], ob[3]))	
				Used[ob]=True

	OBdict = defaultdict(list)
	for referedOB in Used.keys():
		OBdict[referedOB[0]] += [(referedOB[4], referedOB[5])]

	return len(OBdict.keys()), CheckCross(OBdict)


def GetWordRefInfo(line):
	linelist = line.split(',')
	#print linelist, line

	posStr = linelist[1]
	mid = posStr.find('-')
	start=int(posStr[1:mid])
	end = int(posStr[mid+1:len(posStr)-1])

	wordItem = linelist[0]
	return range(start, end+1), wordItem[1:len(wordItem)-1], linelist[2], bool(linelist[3])


def ReadObjectfile(objectfile):
	WordObjectDict = defaultdict(list)
	fin = open(objectfile, 'r')
	while True:
		line = fin.readline()
		if not line:
			break
		line = line.strip()
		if line.find('appear')!=-1:
			match = re.search('<.*>', line)
			matchWord = match.group(0)
			objectName = matchWord[1:len(matchWord)-1]
			refNum = int(line.split()[1].split(':')[1])
			for i in range(0, refNum):
				line = fin.readline().strip()
				posList, word, speaker, ref = GetWordRefInfo(line)
				for pos in posList:
					WordObjectDict[pos] += [(objectName, word, speaker, ref, min(posList), max(posList))]

	fin.close()

	return WordObjectDict

words, annotations, notes = read_annotation_file(NDUfile)

WordObjectDict = ReadObjectfile(objectfile)

NDURefer = defaultdict(list)

outputfile = path.join(outputPath, 'NDUcorrelation.txt')
record = path.join(outputPath, 'NDU-reference.txt')
fout = open(outputfile, 'w')
fout2 = open(record, 'w')
for ai in annotations:
	NDURefer[ai.label] += [ai.name]
	idxList = [int(word.name.split('_')[1]) for word in ai.words]
	obNum, crossNum = output(fout, ai, WordObjectDict, idxList)
	fout.write("<\%s>,%s,%s\n" % (ai.name.split('_')[0], obNum, crossNum))
	fout2.write("%s,%s,%s\n" % (ai.name.split('_')[0], obNum, crossNum))
fout.close()
fout2.close()

countfile = path.join(outputPath, 'NDUdistribution.txt')
f = open(countfile, 'w')
for lb, occur_list in NDURefer.items():
	f.write("%s %s\n" % (lb, len(occur_list)))
f.close()
