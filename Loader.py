#!/usr/bin/env python

from collections import defaultdict
import re

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

def LoadSurfaceLayer(surfacefile):
	surface_info = defaultdict(list)
	fin = open(surfacefile)
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
                                posList, word, spk, ref, ob, gesture = GetWordRefInfo(line)
				surface_info[objectName] += [(word, posList, spk, ob, gesture)]	
	fin.close()
	return surface_info
