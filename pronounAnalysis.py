#!/usr/bin/env python

import sys
sys.path.append('/home/yipeiw/Documents/util')

import pronoun
import Loader

#root='/home/yipeiw/Documents/analysis/CESAR-data-analysis/'
#surfacefile=root + 'result/CESAR_Jun-Sun-3-11-10-36-2012/surfaceLayer.txt'
#outputfile = root + 'result/CESAR_Jun-Sun-3-11-10-36-2012/pronoun.txt'

surfacefile = sys.argv[1]
outputfile = sys.argv[2]

pronounfile = '/home/yipeiw/Documents/baseline/English_Pronoun.list'

pronoun_list = pronoun.LoadPronoun(pronounfile)

surface_info = Loader.LoadSurfaceLayer(surfacefile)

singles = 0
histogram = {}
for ob, expressions in surface_info.items():
	total = len(expressions)
	pronoun_num = 0
	for words, pos_list, spk, lb_name, lb_gesture in expressions:
		if words=="":
			print pos_list, lb_name
		if pronoun.IsPronoun(words, pronoun_list, 'dict') > 0:
			pronoun_num += 1
	if pronoun_num==total:
		singles += 1
	histogram[(ob, lb_name, lb_gesture)]=(total, pronoun_num)

fout = open(outputfile, 'w')
for obInfo, info in histogram.items():
	ob, lb, gesture = obInfo
	total, pronouns = info
	fout.write("%s,%s,%s,%s\n" % (ob, total, pronouns, total-pronouns))
fout.close()
