import spacy
import json
import sys
import os
import IPython
from ipywidgets import widgets
from IPython.display import display
import readability
import spotlight

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
        #print(text_for_pipeline)
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

#FUNCTION C: Extracts all the entities and appends them to the entity categories in the json metadata
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

#def entity_linking();

#FUNCTION D: Maps the POS-tags to the words
def create_dict_of_words_vs_postags():
    global dict_of_words
    dict_of_words = {}
    for word in doc:
        dict_of_words[word.string] = word.tag_

#FUNCTION E: CREATES A FUNCTION THAT GENERATES A DICTIONARY OF CONTENT WORDs (for EMOTION?)
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

#EMOTIONTAGGER: A FUNCTION THAT CALLS THE EMOTIONTAGGER (VOSSEN) VIA A .sh SCRIPT / A .java/.lib FILE

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
        robot_metadata.write(json.dumps(received_data))
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
        robot_metadata.write(json.dumps(received_data))
        robot_metadata.truncate()

#WORDLENGTH MISSING

#READABILITY FUNCT
import readability
text = "We are looking for Richard Franzen, an American who has built a robot, he resides in Tagoyashi."
def structure_processor(text):
    result = readability.getmeasures(text)
    print(result)
    return result
structure_processor()
# MvE to do: output it to the right json format

#MAYBE A CLEANUP FUNCTION FOR POSTPROCESSING (DEMO) CAN BE USEFUL. MUST BE A SELECT
#CLEANING OF KEY-VALUES.... TO BE DECIDED YET
def metadata_cleaning():
    print('Clean it up!')

#ENTER THE NAME OF DEMO INPUT FILE: sample_input.json
def demos_file():
    global filename_widget
    filename_widget = widgets.Text()
    display(filename_widget)
    def handle_submit(sender):
        print(filename_widget.value)
    filename_widget.on_submit(handle_submit)
demos_file()

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

#PROCESSING SEQUENCE 1: Execute all defined the functions
#metadata_cleaning() ---function not defined yet
select_metadata()
with open(metadata, 'r+') as robot_metadata:
    select_text_input()
    received_data = json.load(robot_metadata)
    read_json_metadata()
    global doc
    doc = nlp(text_for_spacy)
    semantic_processing()
    #entity_linking()  ---function not defined yet
    create_dict_of_words_vs_postags()
    create_dict_of_content_words()
    structural_processor()
    #emotion_processing  ---function not defined yet
#SOME MISSING FUNCTIONS