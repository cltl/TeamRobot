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

#with open('json_schema/metadata.json') as data_file:
#	data = json.load(data_file)

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
	try:
		response = server.annotate_and_respond(input)
	except:
		response = "I am sorry, I do not understand"
	response = response.replace("'","-=AP=-")	
	json_dict['response'] = response 
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
