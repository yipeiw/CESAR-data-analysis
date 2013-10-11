#!/usr/bin/env python

import sys
sys.path.append('/home/yipeiw/Documents/Research-2013fall/Tool/AnnotationAnalysis')
import os.path as path
from read_write_annotation_files import *

from collections import defaultdict
import re

#objectfile='/home/yipeiw/Documents/Research-2013fall/sample/object-reference.xml'
#outputPath='/home/yipeiw/Documents/Research-2013fall/LabelAnalysis/result'
objectfile = sys.argv[1]
outputPath = sys.argv[2]

def Normalize(text):
        if text.find('%')!=-1:
                return ""
        return re.sub('[^a-z0-9]', '', text.lower())

def IsAppear(keyword_list, word_text_list):
	for word in keyword_list:
		for sur_word in word_text_list:
			if word==sur_word:
				return True

	return False

def Analyze(surface_list):
	expressionDict = defaultdict(bool)
	expressionHumanDict = defaultdict(bool)
        omitNumHuman = 0
       	omitNum = 0
        appearHuman = 0

	for wordText, omitted, ids, speaker in surface_list:
		expressionDict[wordText]=True
		if speaker=='driver':
			appearHuman += 1
			expressionHumanDict[wordText]=True
        	if omitted:
                	omitNum += 1
                        if speaker=='driver':
                        	omitNumHuman += 1
	Enum = (len(expressionDict.keys()), len(expressionHumanDict.keys()))
	Onum = (omitNum, omitNumHuman)
	appear = (len(surface_list), appearHuman)	
	
	return (appear, Enum, Onum)


def output(outputPath, objectSurface):
	Surface = path.join(outputPath, 'Surface.txt')
	analysisfile = path.join(outputPath, 'surfaceLayer.txt')
	f1 = open(analysisfile, 'w')
	f2 = open(Surface, 'w')
	for ob, surface_list in sorted(objectSurface.items(), key=lambda item:len(item[1]), reverse=True):
		Appear, Expression, Omit = Analyze(surface_list)

		f1.write("<%s> appear_num:%s expression_num:%s omit:%s by_driver_appear:%s by_driver_expression:%s by_driver_omit:%s\n" % (ob, Appear[0], Expression[0], Omit[0], Appear[1], Expression[1], Omit[1]))
		f2.write("%s,%s,%s,%s,%s,%s,%s\n" % (ob, Appear[0], Expression[0], Omit[0], Appear[1], Expression[1], Omit[1]))
		for wordText, omitted, ids, speaker in surface_list:
			f1.write("	<%s>,<%s-%s>,%s,%s\n" % (wordText, min(ids), max(ids), speaker, omitted))
			
	f1.close()
	f2.close()


words, annotations, notes = read_annotation_file(objectfile)

objectSurface = defaultdict(list)

for ai in annotations:
	wordlist = []
	speaker = ai.words[0].speaker
	for word in ai.words:
		idx = int(word.name.split('_')[1])

		wordlist.append( (idx, Normalize(word.text)) )
	word_text_list = [text for idx, text in sorted(wordlist, key=lambda item:item[0])]
	idx_list = [idx for idx, text in sorted(wordlist, key=lambda item:item[0])]
	object_text_list=[Normalize(word) for word in ai.object_parameter.split('_')]
	omitted = IsAppear(object_text_list, word_text_list)	
	objectSurface[ai.object_parameter] += [(" ".join(word_text_list).strip(), omitted, idx_list, speaker)]

output(outputPath, objectSurface)
