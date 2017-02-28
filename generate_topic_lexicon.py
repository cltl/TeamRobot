#!/usr/bin/python

# This is a script that reads in the concordance scores and generates a topic 
# lexicon of the form:
# word	topic	score 
# The score is 0 or 1 
# This is similar to the NRC (National Research Council Canada) emotion lexicon

# marieke.van.erp@vu.nl
# 28 February 2017 

import sys 
import glob 

topic_words = {} 
files = glob.glob('/Users/marieke/Downloads/collocates_for_types/antconc_results_sl_*')
for file in files:
	with open(file, 'r') as f:
		topic = file.replace("/Users/marieke/Downloads/collocates_for_types/antconc_results_sl_","")
		topic = topic.replace(".txt", "")
		if topic == "humor":
			topic = "humour"
		for line in f:
			line = line.rstrip()
			if line.startswith("#"):
				continue
			elems = line.split("\t")
			if elems[4] == "0":
				continue
			if elems[5] in topic_words:
				topic_words[elems[5]][topic] = 1 
			else:
				topic_words[elems[5]] = {}
				topic_words[elems[5]][topic] = 1 
for word in topic_words:
	for topic in topic_words[word]:
		print(word + "\t" + topic + "\t1")
			
			
		
