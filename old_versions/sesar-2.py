
# coding: utf-8

# In[107]:

import os
import sys
import json
import spacy
import pprint
import IPython
import spotlight
import subprocess
from subprocess import call
import readability 
import urllib.parse 
import urllib.request  
from random import randint
from ipywidgets import widgets
from IPython.display import display


# In[49]:

nlp = spacy.load('en')   


# In[89]:

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


# In[90]:

#FUNCTION A: creates a text input from an argument which has to be typed in the following form:
#################  "Hello, this is a new sentence. And this is a newer one"
def select_text_input():
    global text_for_pipeline
    text_from_commandline = str(sys.argv[2:])
    if "/" in text_from_commandline:
        text_for_pipeline = text_widget.value
    elif text_from_commandline:
        text_clean = text_from_commandline.replace("[","")
        text_cleaner = text_clean.replace("'","")
        text_for_pipeline = text_cleaner.replace("]","")
        return text_for_pipeline


# In[91]:

#FUNCTION B: loads a file of .json-format, in order to read the "text input"-value and to modify it. 
def read_json_metadata():
    global robot_metadata
    global text_for_spacy
    global received_data
    text_from_json = received_data["metadata"]["input_text"]
    if text_from_json != 'None':
        received_data["metadata"]["input_text"] = text_for_pipeline
        text_for_spacy = received_data["metadata"]["input_text"]
        robot_metadata.seek(0)
        robot_metadata.write(json.dumps(received_data, sort_keys = True,  indent=4))
        robot_metadata.truncate()
        print('Text voor SpaCy:', text_for_spacy)


# In[92]:

#FUNCTION C: Matches (a) given string(s) to an entity in DBPedia. Returns the structured data of the entity 
#in the form of a dictionary
def link_to_dbpedia(doc):
    query = doc
    urlPostPrefixSpotlight = "http://spotlight.sztaki.hu:2222/rest/annotate"
    args = urllib.parse.urlencode([("text", query), ("confidence", 0), ("support", 0)]).encode("utf-8")
    request = urllib.request.Request(urlPostPrefixSpotlight, data=args, headers={"Accept": "application/json"})
    response = urllib.request.urlopen(request).read()
    dbpedia_ent_dict = json.loads(response.decode('utf-8'))
    return dbpedia_ent_dict


# In[93]:

#FUNCTION D: Extracts the metadata of the entity in Matches (a) given string(s) to an entity in DBPedia.
def extract_entity_values(entity):
    dbp_resrc = entity['Resources']
    for dbp_resrc_dict in dbp_resrc:
        ent_name_in_dbp = dbp_resrc_dict['@surfaceForm']
        ent_type_in_dbp = dbp_resrc_dict['@types']
        ent_uri_in_dbp = dbp_resrc_dict['@URI']
        ent_conf_in_dbp = dbp_resrc_dict['@similarityScore']
        dbp_resrc_dict
        return (ent_name_in_dbp, ent_type_in_dbp, ent_uri_in_dbp, ent_conf_in_dbp)


# In[94]:

def create_entity_dict(selected_values):
    dbp_keys = ('name','type','URI','confidence')
    ent_dict = dict(zip(dbp_keys, selected_values))
    ent_id = 'ent'+str(randint(0,100))
    dict_of_defined_entity = {}
    dict_of_defined_entity[ent_id] = ent_dict
    return dict_of_defined_entity    


# In[95]:

def semantic_processing_with_dpbedia():
    for entity in doc.ents:
        entity_in_dbpedia = link_to_dbpedia(entity)
        dbp_values = extract_entity_values(entity_in_dbpedia)
        interpreted_entity = create_entity_dict(dbp_values)
        if entity.label_ == 'GPE':
            received_data['semantic']['places'].update(interpreted_entity)
        if entity.label_ == 'ORG':
            received_data['semantic']['organisations'].update(interpreted_entity)
        if entity.label_ == 'PERSON':
            received_data['semantic']['people'].update(interpreted_entity)
        robot_metadata.seek(0)
        robot_metadata.write(json.dumps(received_data, sort_keys = True, indent=4))
        robot_metadata.truncate()


# In[96]:

def create_dict_of_words_vs_postags():
    global dict_of_words
    dict_of_words = {}
    for word in doc:
        dict_of_words[word.string] = word.tag_


# In[97]:

#CREATES A FUNCTION THAT GENERATES A DICTIONARY OF CONTENT WORD (EMOTION?)
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


# In[121]:

os.system('./script.sh')


# In[99]:

#STRUCTURAL PROCESSOR (FUNCTION) NEEDS TO BE DEFINED
def structural_processor(): 
    received_data['structure']['wordcount'] = int(len(dict_of_words))
    for sent in doc.sents:
        received_data['structure']['number_of_sentences'] += 1    
    for word in doc:      
        if 'JJ' in word.tag_:
            received_data['structure']['adjective_count'] += 1 
        if 'RB' in word.tag_:
            received_data['structure']['adverbs'] += 1
        if 'PRP' in word.tag_:
            received_data['structure']['personal_pronouns'] += 1
        if 'VBD' in word.tag_:
            received_data['structure']['non_future'] += 1
        if 'VBN' in word.tag_:
            received_data['structure']['non_future'] += 1
        if 'VB' in word.tag_: 
            received_data['structure']['future'] += 1
        if 'VBG' in word.tag_:
            received_data['structure']['future'] += 1            
        if 'VBP' in word.tag_: 
            received_data['structure']['future'] += 1
        if 'VBZ' in word.tag_:  
            received_data['structure']['future'] += 1
        robot_metadata.seek(0)
        robot_metadata.write(json.dumps(received_data, sort_keys = True, indent=4))
        robot_metadata.truncate()
    for dependancy in doc:
        if dependancy.dep_ == 'neg':
            received_data['structure']['negations'] += 1
        if dependancy.dep_ == 'prep':
            received_data['structure']['prepositional_phrases_count'] += 1
        if dependancy.dep_ == 'aux':
            received_data['structure']['active_sentences'] += 1
        if dependancy.dep_ == 'auxpass':
            received_data['structure']['passive_sentences'] += 1
        robot_metadata.seek(0)
        robot_metadata.write(json.dumps(received_data, sort_keys = True, indent=4))
        robot_metadata.truncate()


# In[100]:

#ENTER THE NAME OF DEMO INPUT FILE: sample_input.json
def demos_file():
    global filename_widget
    filename_widget = widgets.Text()
    display(filename_widget)
    def handle_submit(sender):
        print(filename_widget.value)        
    filename_widget.on_submit(handle_submit) 
demos_file()


# In[101]:

#ENTER THE NAME OF DEMO INPUT FILE: We are looking for Richard Franzen an American who has built a robot.
################################### He resides in Tagoyashi.
def demos_text():
    global text_widget
    text_widget = widgets.Text()
    display(text_widget)
    def handle_submit(sender):
        print(text_widget.value)        
    text_widget.on_submit(handle_submit)
demos_text()


# In[102]:

#PROCESSING SEQUENCE 1: Execute all defined the functions
#metadata_cleaning() ---function not defined yet
select_metadata()
with open(metadata, 'r+') as robot_metadata:  
    select_text_input()
    received_data = json.load(robot_metadata)
    read_json_metadata()
    global doc
    doc = nlp(text_for_spacy)
    semantic_processing_with_dpbedia()
    create_dict_of_words_vs_postags()
    create_dict_of_content_words() 
    structural_processor()        
    emotion_processing  ---function not defined yet
#SOME MISSING FUNCTIONS


# In[ ]:

#READABILITY FUNCT
#import readability 
#text = "We are looking for Richard Franzen, an American who has built a robot, he resides in Tagoyashi."
#def structure_processor(text):
#    result = readability.getmeasures(text)
#    print(result)
#    return result  
#structure_processor()
# MvE to do: output it to the right json format 

