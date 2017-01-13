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

xmlfile = sys.argv[1] 
tree = etree.parse(xmlfile)
try: 
	author = tree.findall('.//contrib')
	for i in author:
		for element in i.iter("string-name"):
			sys.stdout.write("Author: " + element.text + "\n")	
except: 
	pass
try:
	institution = tree.findall('.//institution')
	for i in institution:
		sys.stdout.write("Institution: " + i.text + "\n")	
except:
	pass
try:
	title = ""
	title = tree.find('.//article-title')
	ys.stdout.write("Title: " + title.text + "\n")
except:
	pass 
try:
	abstract = ""
	abstract = tree.find('.//abstract')
	for element in abstract.iter():
		abstract_text = element.text.lstrip()
		sys.stdout.write("Abstract: " + abstract_text + "\n")
except:
	pass
try:
	references = "" 
	references = tree.findall('.//ref')
	for reference in references:
		for element in reference.iter('article-title'):
			sys.stdout.write('Reference_title: ' + element.text + "\n")
		for element in reference.iter('string-name'):
			name_string = '' 
			for name in element.iter():
				name_string = name.text + " "  + name_string 
			name_string = name_string.lstrip()
			name_string = name_string.rstrip()
			sys.stdout.write("Author: " + name_string + "\n")
except:
	pass


