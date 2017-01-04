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
import pprint
import subprocess
from subprocess import call, Popen, PIPE
from random import randint
import urllib.parse
import urllib.request
import os
import readability
import response_module as rmod

# A small warning that it may take a while for the data to load
print('------------\nLoading the language model, this may take a while\n\n-------------\n')

# Make sure the spacy module is loaded (this may take a while)
nlp = spacy.load('en')

def annotate(text):
    doc = nlp(text)
    entities = {}
    for i in doc.ents:
        entities[i.text] = i.ent_type_
        outputstring = "What is " + i.text
        os.system("say " + outputstring)
        print(i.text, i.ent_type_)

# Commands to deal with the input & output
def getcmd(cmdlist):
    cmd = input('\nP3PP3R:> ')
    if cmd == 'quit':
        exit(0)
    annotate_and_respond(cmd)

def start():
    print('\n-------')
    cmd = getcmd(input)
    start()

def structure_processor(text):
    result = readability.getmeasures(text)
    return result

# This is where the text annotation takes place
# copied from Yassine's code

def select_metadata():
    global metadata
    metadata = str(sys.argv[1])
    if "-f" in metadata:
        metadata = filename_widget.value
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
    elif text_from_commandline:
        text_clean = text_from_commandline.replace("[","")
        text_cleaner = text_clean.replace("'","")
        text_for_pipeline = text_cleaner.replace("]","")
        return text_for_pipeline

# Link entities to DBpedia
# To do: revert to local server
def link_to_dbpedia(doc):
    query = doc
    urlPostPrefixSpotlight = "http://spotlight.sztaki.hu:2222/rest/annotate"
    args = urllib.parse.urlencode([("text", query), ("confidence", 0), ("support", 0)]).encode("utf-8")
    request = urllib.request.Request(urlPostPrefixSpotlight, data=args, headers={"Accept": "application/json"})
    response = urllib.request.urlopen(request).read()
    dbpedia_ent_dict = json.loads(response.decode('utf-8'))
    return dbpedia_ent_dict

# Recognise enities
def extract_entity_values(entity):
    try:
        dbp_resrc = entity['Resources']
        for dbp_resrc_dict in dbp_resrc:
            ent_name_in_dbp = dbp_resrc_dict['@surfaceForm']
            ent_type_in_dbp = dbp_resrc_dict['@types']
            ent_uri_in_dbp = dbp_resrc_dict['@URI']
            ent_conf_in_dbp = dbp_resrc_dict['@similarityScore']
            dbp_resrc_dict
    except:
        ent_name_in_dbp = ''
        ent_type_in_dbp = ''
        ent_uri_in_dbp = ''
        ent_conf_in_dbp = ''
    return (ent_name_in_dbp, ent_type_in_dbp, ent_uri_in_dbp, ent_conf_in_dbp)

# Create a dictionary to organise the entity links
def create_entity_dict(selected_values):
    dbp_keys = ('name','type','URI','confidence')
    ent_dict = dict(zip(dbp_keys, selected_values))
    ent_id = 'ent'+str(randint(0,100))
    dict_of_defined_entity = {}
    dict_of_defined_entity[ent_id] = ent_dict
    return dict_of_defined_entity

# Bring it together
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
        outputfile.write(json.dumps(received_data, sort_keys = True, indent=4))

# Also get the part of speech tags and make sure there is a structure for them
def create_dict_of_words_vs_postags():
    global dict_of_words
    dict_of_words = {}
    for word in doc:
        dict_of_words[word.string] = word.tag_

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

# Tag emotions (with Piek's emotion tagger)
def emotion_processor(text_input):
    sentence = text_input #"I am very mad and very very angry at the stupid painful losing Barack Obama in Washigngton DC when he was working with Microsoft in Paris."
    modifier_dict = {}
    emotions_dict = {}
    emotions_score_dict = {}
    proc = subprocess.Popen([ 'echo {} | ./emotionStream.sh'.format(sentence)], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    modif_output = out.decode().split('],')[1]
    modif_label = modif_output.split(":[")[1:]
    modif = modif_label[0]
    modifiers_as_string = modif.strip("{}}]")
    modifiers = modifiers_as_string.split(",")
    for modifier in modifiers:
        item, value = modifier.split(":")
        item = item.strip('"')
        value = int(value.strip('"'))
        modifier_dict[item] = value
    emo_output = out.decode().split('],')[0]
    emo_label = emo_output.split(":[")[1:]
    emo = emo_label[0]
    emo_as_string = emo.strip("{}}]")
    emotions = emo_as_string.split(",")
    for emotion in emotions:
        item, value = emotion.split(":")
        item = item.strip('"')
        value = int(value.strip('"'))
        emotions_dict[item] = value
    for key, value in emotions_dict.items():
        if value != 0:
            emotions_score_dict[key] = value
    return emotions_score_dict

# And write them neatly to a file
def emotions_extraction(target_emo_dict):
    emotions_score_dict_to_process = target_emo_dict
    for emotion,value in emotions_score_dict_to_process.items():
        received_data['emotions']['detected_emotion'].append(emotion)
        outputfile.write(json.dumps(received_data, sort_keys = True, indent=4))

# Gather stats about the structure of the conversation
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
        outputfile.write(json.dumps(received_data, sort_keys = True, indent=4))
    for dependency in doc:
        if dependency.dep_ == 'neg':
            received_data['structure']['negations'] += 1
        if dependency.dep_ == 'prep':
            received_data['structure']['prepositional_phrases_count'] += 1
        if dependency.dep_ == 'aux':
            received_data['structure']['active_sentences'] += 1
        if dependency.dep_ == 'auxpass':
            received_data['structure']['passive_sentences'] += 1
        outputfile.write(json.dumps(received_data, sort_keys = True, indent=4))

#PROCESSING PIPELINE: Execute all defined functions and modules:
def annotate_and_respond(text):
    global robot_metadata
    counter = str(randint(0,100))
    global outputfile
    #received_data['process_state'] = 'processed'
    outputfile_name = 'processed/processed_sentence_' + counter + '.json'
    outputfile = open(outputfile_name, 'w')
    with open('metadata.json', 'r+') as robot_metadata:
        global received_data
        received_data = json.load(robot_metadata)
        print(received_data)
        global doc
        doc = nlp(text)
        semantic_processing_with_dpbedia()
        create_dict_of_words_vs_postags()
        create_dict_of_content_words()
        structural_processor()
        processed_emotion = emotion_processor(doc)
        emotions_extraction(processed_emotion)
        generated_response = rmod.generate_response(received_data['semantic'])
        received_data['response'] = generated_response
        print(generated_response)
        os.system("say " + generated_response)
        outputfile.write(json.dumps(received_data, sort_keys = True, indent=4))
        outputfile.close()
        rmod.generate_response(received_data['semantic'])

# Run the whole thing
if __name__ == "__main__":
    start()