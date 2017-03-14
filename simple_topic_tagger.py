#!/usr/bin/python 

# This is a very basic topic tagger 
# marieke.van.erp@vu.nl
# 28 February 2017

import sys 

topics = {}
with open('topic_lexicon.tsv', 'r') as f:
	for line in f:
		line = line.rstrip()
		elems = line.split("\t")
		if elems[1] in topics:
			topics[elems[1]][elems[0]] = 1
		else:
			topics[elems[1]] = {}
			topics[elems[1]][elems[0]] = 1
			
test = """well it sometimes I chords what do I want to do after anything my study"""

def annotate_topic(text):
	text_topic = {}
	tokens = text.lower().split(" ")
	for token in tokens:
		for topic in topics:
			if token in topics[topic]:
				if topic in text_topic:
					text_topic[topic] = text_topic[topic] + 1 
				else:
					text_topic[topic] = 1 
	return text_topic 
	
text_topics = annotate_topic(test)
res = list(sorted(text_topics, key=text_topics.__getitem__, reverse=True))
print(res[0])
