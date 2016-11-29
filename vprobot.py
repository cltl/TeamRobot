import spacy
import json
import sys
import os
import IPython
from ipywidgets import widgets
from IPython.display import display

nlp = spacy.load('en')   

def select_metadata():
    global metadata
    metadata = str(sys.argv[1:])
    if "-f" in metadata:
        metadata = filename_widget.value
        print(metadata)
    else:
        filename_clean = metadata.replace("[","")
        filename_cleaner = filename_clean.replace("'","")
        metadata = filename_cleaner.replace("]","")
        return metadata    

#FUNCTION A: creates a text input from an argument which has to be typed in the following form:
#################  "Hello, this is a new sentence. And this is a newer one"
def select_text_input():
    global text_for_pipeline
    text_from_commandline = str(sys.argv[2:])
    if "/" in text_from_commandline:
        text_for_pipeline = text_widget.value
        print(text_for_pipeline)
    elif text_from_commandline:
        text_clean = text_from_commandline.replace("[","")
        text_cleaner = text_clean.replace("'","")
        text_for_pipeline = text_cleaner.replace("]","")
        return text_for_pipeline

#FUNCTION B: loads a file of .json-format, in order to read the "text input"-value and to modify it. 
def read_json_metadata():
    global robot_metadata
    global text_for_spacy
    global received_data
    #with open(json_schema, 'r+') as robot_metadata:
    #received_data = json.load(robot_metadata)
    text_from_json = received_data["metadata"]["input_text"]
    if text_from_json != 'None':
        received_data["metadata"]["input_text"] = text_for_pipeline
        text_for_spacy = received_data["metadata"]["input_text"]
        robot_metadata.seek(0)
        robot_metadata.write(json.dumps(received_data))
        robot_metadata.truncate()
        print('Text voor SpaCy:', text_for_spacy)

#FUNCTION C: Extracts all the entities and appends them to the 3 categories of entities in the json metadata
#object: GPE = Location, ORG = Organization and PERSON.
def semantic_processing():
    for entity in doc.ents:
        if entity.label_ == 'GPE':
            received_data['semantic']['places'].append(str(entity))
            #print(entity, entity.label_)
        if entity.label_ == 'ORG':
            received_data['semantic']['organisations'].append(str(entity))
            #print(entity, entity.label_)
        if entity.label_ == 'PERSON':
            received_data['semantic']['people'].append(str(entity))
            #print(entity, entity.label_)
            robot_metadata.seek(0)
            robot_metadata.write(json.dumps(received_data))
            robot_metadata.truncate()

def create_dict_of_words():
    global dict_of_words
    dict_of_words = {}
    for word in doc:
        dict_of_words[word.string] = word.tag_
    print(dict_of_words)

def create_dict_of_content_words():
    global dict_of_content_words
    dict_of_content_words = {}
    for word in doc:
        if 'NN' in word.tag_:
            dict_of_content_words[word.string] = word.tag_
        if 'VB' in word.tag_:
            dict_of_content_words[word.string] = word.tag_
        if 'JJ' in word.tag_:
            dict_of_content_words[word.string] = word.tag_
        if 'RB' in word.tag_:
            dict_of_content_words[word.string] = word.tag_

#PROCESSING SEQUENCE 1: Execute all defined the functions
#Process the text with the SpaCy Pipeline 
select_metadata()
with open(metadata, 'r+') as robot_metadata: 
    select_text_input()
    received_data = json.load(robot_metadata)
    read_json_metadata()
    global doc
    doc = nlp(text_for_spacy)
    semantic_processing()
    create_dict_of_words()
    create_dict_of_content_words()
    
