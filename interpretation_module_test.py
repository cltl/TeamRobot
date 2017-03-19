#!/usr/bin/python 

# This script takes a file with one utterance per line and generates a response
# Can be used for testing the approach  

import urllib.request
import requests 
import server_tecs as server
import json 
import subprocess
import ast
import sys

# Quick hack to get the topic tagger in there 
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
	
# Simple topic tagger 
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


with open(sys.argv[1], 'r') as file:
	for line in file:
		line = line.rstrip()
		input = line.lower()
		input = input.replace("n't"," not")
		input = input.replace("'s", " is")
		input = input.replace("\\", " ")
		input = input.replace("'", " ")
		print("INPUT: ", input)
		response = ""
		topic_res = "" 
		try:
			response = server.annotate_and_respond(input)
		except:
			response = "No fitting response found"
		try:
			text_topics = annotate_topic(input)
			res = list(sorted(text_topics, key=text_topics.__getitem__, reverse=True))
			topic_res = res[0]
		except:
			topic_res = "NO TOPIC FOUND"
		response = response.replace("'","-=AP=-")	
		topic_response = "What is " + topic_res + "?"
		print("CONCEPT_response: ", response, "\n", "TOPIC_Marieke: ", topic_response, "\n\n") 
		


