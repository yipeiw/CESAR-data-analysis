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

def GetWordRefInfo(line):
	linelist = line.split(',')
	#print linelist, line

	posStr = linelist[1]
	mid = posStr.find('-')
	start=int(posStr[1:mid])
	end = int(posStr[mid+1:len(posStr)-1])

	wordItem = linelist[0]
	ob = linelist[len(linelist)-1]
	ob_delimit = ob.find('(')
	ob_class = ob[0:ob_delimit].strip()
	ob_gesture = ob[ob_delimit+1:len(ob)-1]
	gesture = (ob_gesture.find("No")==-1)
	return (range(start, end+1), wordItem[1:len(wordItem)-1], linelist[2], bool(linelist[3]), ob_class, gesture)

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
				posList, word, speaker, ref, ob, gesture = GetWordRefInfo(line)
				for pos in posList:
					WordObjectDict[pos] += [(objectName, ob, word, speaker, ref, gesture, min(posList), max(posList))]

	fin.close()

	return WordObjectDict

def GetOB(words):
	occur = defaultdict(bool)
	for word in words:
		idx = int(word.name.split('_')[1])
		for infolist in WordObjectDict[idx]:	
			(ob_name, ob_class, word, spk, ref, gesture, start, end) = infolist
			occur[ob_class] = True
	return occur.keys()
	
words, annotations, notes = read_annotation_file(NDUfile)
WordObjectDict = ReadObjectfile(objectfile)

#estimate P(NDU_i), P(NDU_i|NDU_j)
#estimate P(ob_class|NDU_i)
unigram = defaultdict(int)
bigram = defaultdict(int)
emit = defaultdict(int)
pre="START"
unigram[pre] += 1
for ai in annotations:
	unigram[ai.label] += 1
	bigram[(pre, ai.label)] += 1
	for ob in GetOB(ai.words):
		emit[(ob, ai.label)] += 1
	pre = ai.label

output_unigram = path.join(outputPath, 'distribution.txt')
f1 = open(output_unigram, 'w')
total = sum([number for number in unigram.values()])
for name, number in sorted(unigram.items(), key=lambda item:item[1], reverse=True):
	f1.write("%s,%.3f\n" % (name, float(number)/total))
f1.close()

output_bigram = path.join(outputPath, 'transition.txt')
f2 = open(output_bigram, 'w')
for pair, prob in bigram.items():
	(pre, current) = pair
	transit = float(prob)/unigram[pre]
	f2.write("%s|%s,%.3f\n" % (current, pre, transit))
f2.close()

output_emit = path.join(outputPath, 'emit.txt')
f3 = open(output_emit, 'w')
for pair, num in emit.items():
	(ob, NDU) = pair
	emit_prob = float(num)/unigram[NDU]
	f3.write("%s|%s,%.3f\n" % (ob, NDU, emit_prob))
f3.close()

