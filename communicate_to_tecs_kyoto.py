#!/usr/bin/python 

# This script listens to the TECS server (through Paul Huygen's intermediate 
# server, processes the text and sends it back  

# Server waiting: http://178.18.83.6:5000/waitfor 

import urllib.request
import requests 
import server_tecs as server
import json 
import subprocess
import ast

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

while True:
	text = subprocess.Popen("get_ASR_text", shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").split("\n")
	# Check 
	print(text)
	json_dict = ast.literal_eval(text[0]) 
	input = json_dict['input']['input_text']['text']
	input = input.lower()
	input = input.replace("n't"," not")
	input = input.replace("'s", " is")
	input = input.replace("'", " ")
	json_dict['input']['input_text']['text'] = json_dict['input']['input_text']['text'].replace("'","-=AP=-")
	print(input)
	response = ""
	topic_res = "" 
	try:
		response = server.annotate_and_respond(input)
	except:
		response = "I am sorry, I do not understand"
	try:
		text_topics = annotate_topic(test)
		res = list(sorted(text_topics, key=text_topics.__getitem__, reverse=True))
		topic_res = res[0]
	except:
		topic_res = "AI"
	response = response.replace("'","-=AP=-")	
	json_dict['response'] = response 
	json_dict['topic_response'] = "What is " + topic_res + "?"
	output = json.dumps(json_dict)
	print(output)
	#subprocess.Popen(["echo", output, "|", "send_VU_processed"], stdout=subprocess.PIPE)
	command = "echo '" + output + "' | send_VU_processed" 
	subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8").split("\n")
	#r = requests.post(url, data=data, allow_redirects=True) 
	#print(r.content) 

#url = 'http://178.18.83.6:5000/send'
#response = server.annotate_and_respond(string)
#data['response'] = response
#send_back = {'VU_processed': data}
#r = requests.post(url, data=data, allow_redirects=True) 
#print(r.content)


#subprocess.Popen("send_VU_processed", shell=True, #stdin=subprocess.PIPE).stdout.read().decode("utf-8").split("\n")
