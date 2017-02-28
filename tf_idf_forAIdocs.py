from __future__ import division
import string
import math
import glob
import sys
import re 
import math 
import json

# Read in the concept list
with open('dark.json') as data_file:
	data = json.load(data_file)

conceptlist = {}
for instance in data['instance']:
	for label in instance['labels']:
		label = re.sub(r'\W+', '', label)
		tokens = label.lower().split(" ")
		for token in tokens: 
			conceptlist[token.lower()] = 0 

# Read in the files and update counter if a concept occurs in the document
df = {} 
files = glob.glob('/mnt/scistor1/group/projects/teamrobot/ai_nafs/*txt')
words = []
NumberDocs = len(files) 
for file in files:
	for line in file:
		line = line.rstrip()
		line = re.sub(r'\W+', '', line)
		tokens = line.lower().split(" ")
		for token in tokens:
			words.append(token)
	unique = set(words)
	for concept in conceptlist:
		if concept in unique:
			if concept in df:
				df[concept] = df[concept] + 1 
			else:
				df[concept] = 1 
	
idf = {} 				
for concept in df:
	 try:
	 	temp = NumberDocs / df[concept]
	 	idf[concept] = math.log10(temp) 
	 except:
	 	idf[concept] = 0 
	 
for concept in idf:
	print(concept + "\t" + idf[concept]) 

	 	
	
	
					
			
	
		
