#!/usr/bin/python 

# This script is meant to demo the VPRO robot conversation 
# It is very basic and starts a prompt in which a user can type some text
# This text is enriched with semantic information after which a suitable response or 
# set of responses is returned 

# Author: Marieke.van.Erp@vu.nl
# Date: 9 December 2016 

import spacy
import json
import sys
import os
import readability 

# A small warning that it may take a while for the data to load 
print('------------\nLoading the language model, this may take a while\n\n-------------\n')

# Make sure the spacy module is loaded (this may take a while) 
nlp = spacy.load('en') 

def annotate(text):
	doc = nlp(text)
	entities = {} 
	for i in doc: 
		if len(i.ent_type_) > 0:
			entities[i.text] = i.ent_type_  
			print(i.text, i.ent_type_)

def getcmd(cmdlist):
	cmd = input('\nP3PP3R:> ')
	annotate(cmd)
			
def start():
	print('\n-------')
	cmd = getcmd(input)
	start()
	
def structure_processor(text):
    result = readability.getmeasures(text)
    return result 
        
    
if __name__ == "__main__":
    start()    