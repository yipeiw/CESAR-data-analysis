#!/usr/bin/env python

from collections import defaultdict
from nltk import word_tokenize

def LoadPronoun(pronounfile):
	pronoun_dict = defaultdict(bool)
	for line in open(pronounfile):
		linelist = line.strip().split(",")
		if linelist[len(linelist)-1].find("PT")!=-1:
			person = int(linelist[len(linelist)-1].split(":")[1])
			if person==1 or person==2:
				continue
		pronoun_dict[linelist[0]] = True
	return pronoun_dict

def IsPronoun(words, pronoun_list, kind):
	for token in word_tokenize(words):
		if pronoun_list[token]:
			return True
	return False
