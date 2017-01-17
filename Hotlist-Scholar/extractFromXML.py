#!/usr/bin/python

# This script reads in the output of CERMINE and extracts the following:
# Author
# Title
# Institution
# Abstract
# References
# 	Authors
# 	Titles 
# 
# And generates a json structure out of that 
# 
# Date: 12 January 2017
# Author: marieke.van.erp@vu.nl 

from lxml import etree  
import sys 
import json 

data = {}
episode = 'episode_1' 
xmlfile = sys.argv[1] 
tree = etree.parse(xmlfile)
data[episode] = {}
data[episode][xmlfile] = {}
data[episode][xmlfile]['authors']= {}
data[episode][xmlfile]['title']= ''
data[episode][xmlfile]['abstract']= ''
data[episode][xmlfile]['keywords']= []
data[episode][xmlfile]['references']= {}
try: 
	author = tree.findall('.//contrib')
	for i in author:
		for element in i.iter("string-name"):
			#sys.stdout.write("Author: " + element.text + "\n")
			data[episode][xmlfile]['authors']['name'] = element.text 	
except: 
	pass
try:
	institution = tree.findall('.//institution')
	for i in institution:
		#sys.stdout.write("Institution: " + i.text + "\n")	
		data[episode][xmlfile]['authors']['institution'] = i.text
except:
	pass
try:
	title = ""
	title = tree.find('.//article-title')
	#ys.stdout.write("Title: " + title.text + "\n")
	data[episode][xmlfile]['title']= title.text
except:
	pass 
try:
	abstract = ""
	abstract = tree.find('.//abstract')
	for element in abstract.iter():
		abstract_text = element.text.lstrip()
		#sys.stdout.write("Abstract: " + abstract_text + "\n")
		data[episode][xmlfile]['abstract']= abstract_text 
except:
	pass
try: 
	keywords = tree.findall('.//kwd-group')
	for i in keywords:
		for element in i.iter("kwd"):
			#sys.stdout.write("Author: " + element.text + "\n")
			data[episode][xmlfile]['keywords'].append(element.text) 	
except: 
	pass
try:
	references = "" 
	references = tree.findall('.//ref')
	for reference in references:
		for element in reference.iter('article-title'):
			#sys.stdout.write('Reference_title: ' + element.text + "\n")
			data[episode][xmlfile]['references']['reference_title'] = element.text 
		for element in reference.iter('string-name'):
			name_string = '' 
			for name in element.iter():
				name_string = name.text + " "  + name_string 
			name_string = name_string.lstrip()
			name_string = name_string.rstrip()
			#sys.stdout.write("Author: " + name_string + "\n")
			data[episode][xmlfile]['references']['reference_author'] = name.string 
			
except:
	pass

#print(json.dumps(json_data, indent=8) )
sys.stdout.write(json.dumps(data, sort_keys=True, indent=4))
