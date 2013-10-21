#!/usr/bin/env python

import sys
sys.path.append('/home/yipeiw/Documents/Research-2013fall/Tool/AnnotationAnalysis')
import os.path as path
from read_write_annotation_files import *

from collections import defaultdict
import re

objectfile=sys.argv[1]
outputfile=sys.argv[2]

def GetContextWindow(words, win, upper):
	idlist = [int(word.name.split('_')[1]) for word in words]
	left = min(idlist)
	right = max(idlist)
	left_win = (max(0, left-win), left-1)
	right_win = (right+1, min(upper, right+win))
	return left_win, right_win

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

def GetContext(pre_list, post_list, word_map):
	pre_context = " ".join([word_map[idx] for idx in range(pre_list[0], pre_list[1]+1)])
	post_context = " ".join([word_map[idx] for idx in range(post_list[0], post_list[1]+1)])
	return pre_context, post_context

words, annotations, notes = read_annotation_file(objectfile)
word_map = {int(word.name.split('_')[1]): word.text for word in words} 
upper = len(word_map.keys())-1

win=2
record = defaultdict(list)
for ai in annotations:
	if ai.label.find("Road")==-1 and ai.label.find("Traffic")==-1 and ai.label.find("Building")==-1:
		continue

	pre_list, post_list = GetContextWindow(ai.words, win, upper)
	word_dict = {int(word.name.split('_')[1]):word.text for word in ai.words}
	word_text = " ".join([text for idx, text in word_dict.items()])
	pre, post = GetContext(pre_list, post_list, word_map)
	record[word_text] += [(pre, post)]

fout = open(outputfile, 'w')
for text, context_list in record.items():
	for pre, post in context_list:
		fout.write("%s,%s,%s\n" % (text, pre, post))
fout.close()
