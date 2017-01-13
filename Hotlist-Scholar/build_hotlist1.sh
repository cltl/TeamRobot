#!/usr/bin/bash

# Hotlist 1: information about topics and people discussed in the episode
# Date: 12 January 2017
# Author: marieke.van.erp@vu.nl 

# First run the scholar.py script to obtain links to papers written by a particular person 
echo "Gathering citations for Miles Brundage" 
python3 scholar.py -c 15 -a "Miles Brundage" --csv-header | gcut -f7 -d"|" | grep -v "None" > papers.txt 

# Download PDFs 
echo "Downloading PDFs"
cd papers/
wget -i ../papers.txt --restrict-file-names=ascii
cd ..

echo "Converting PDF to XML"
# Run CERMINE PDF Extractor 
cd CERMINE/cermine-impl/target/
java -cp cermine-impl-1.12-SNAPSHOT-jar-with-dependencies.jar pl.edu.icm.cermine.ContentExtractor -path ../../../papers/

echo "Extracting useful things from XML" 
# Run XML extraction script to extract authors, institution, references, titles and 
# abstracts from the files and write output to json structure 
cd ../../../
for x in papers/*cermxml ; do python extractFromXML.py $x >> HotList1.txt ; done 