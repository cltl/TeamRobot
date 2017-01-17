#!/usr/bin/bash

# Hotlist 1: information about topics and people discussed in the episode
# Date: 12 January 2017
# Author: marieke.van.erp@vu.nl 

# First run the scholar.py script to obtain links to papers written by a particular person 
echo "Gathering citations for Anders Sandberg" 
python3 scholar.py -c 15 -a "Anders Sandberg" --csv-header | gcut -f7 -d"|" | grep -v "None" > papers.txt 
echo "Gathering citations for Nick Bostrom" 
python3 scholar.py -c 15 -a "Nick Bostrom" --csv-header | gcut -f7 -d"|" | grep -v "None" >> papers.txt
echo "Gathering citations for Miles Brundage" 
python3 scholar.py -c 15 -a "Miles Brundage" --csv-header | gcut -f7 -d"|" | grep -v "None" >> papers.txt
echo "Gathering citations for David Kenyon" 
python3 scholar.py -c 15 -a "David Kenyon" --csv-header | gcut -f7 -d"|" | grep -v "None" >> papers.txt
echo "Gathering citations for Simon Colton" 
python3 scholar.py -c 15 -a "Simon Colton" --csv-header | gcut -f7 -d"|" | grep -v "None" >> papers.txt
echo "Gathering citations for Rolf Noskwith" 
python3 scholar.py -c 15 -a "Rolf Noskwith" --csv-header | gcut -f7 -d"|" | grep -v "None" >> papers.txt
echo "Gathering citations for Tony Ellis" 
python3 scholar.py -c 15 -a "Tony Ellis" --csv-header | gcut -f7 -d"|" | grep -v "None" >> papers.txt
echo "Gathering citations for Kathleen Richardson" 
python3 scholar.py -c 15 -a "Kathleen Richardson" --csv-header | gcut -f7 -d"|" | grep -v "None" >> papers.txt


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
for x in papers/*cermxml ; do python extractFromXML.py $x > $x.json ; done 

# Merge json files 
# Make sure there is a file called hotlist1.json that only contains {} 
for x in papers/*json ; do jq -s '.[0] * .[1]' hotlist1.json $x > hotlist_tmp ; mv hotlist_tmp hotlist1.json ; done 

