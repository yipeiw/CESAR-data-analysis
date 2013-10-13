#!/usr/bin/env python

import sys
sys.path.append('/home/yipeiw/Tool/iwsds_analysis_tools')
import os.path as path
from read_write_annotation_files import *

from collections import defaultdict
import re
sys.path.append('/home/yipeiw/Documents/util')
import clean
import TextProcess

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

	for wordText, omitted, ids, speaker, lb in surface_list:
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
	analysisfile = path.join(outputPath, 'surfaceLayer.txt')
	f1 = open(analysisfile, 'w')
	for ob, surface_list in sorted(objectSurface.items(), key=lambda item:len(item[1]), reverse=True):
		Appear, Expression, Omit = Analyze(surface_list)

		f1.write("<%s> appear_num:%s expression_num:%s omit:%s by_driver_appear:%s by_driver_expression:%s by_driver_omit:%s\n" % (ob, Appear[0], Expression[0], Omit[0], Appear[1], Expression[1], Omit[1]))
		for wordText, omitted, ids, speaker, label in surface_list:
			f1.write("	<%s>,<%s-%s>,%s,%s,%s\n" % (wordText, min(ids), max(ids), speaker, omitted, label))
			
	f1.close()


words, annotations, notes = read_annotation_file(objectfile)
annotations = clean.PostProcessAnnotation(annotations)

objectSurface = defaultdict(list)

for ai in annotations:
	wordlist = []
	speaker = ai.words[0].speaker

	word_text = " ".join([TextProcess.Denoise(word.text) for word in ai.words])
	idx_list =[int(word.name.split('_')[1]) for word in ai.words]
	object_text_list=[Normalize(word) for word in ai.object_parameter.split('_')]
	omitted = IsAppear(object_text_list, word_text.split())	
	if word_text != "":
		objectSurface[ai.object_parameter] += [ (word_text, omitted, idx_list, speaker, ai.label)]

output(outputPath, objectSurface)
