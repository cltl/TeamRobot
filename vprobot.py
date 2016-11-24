
# coding: utf-8

# Mohammed Yassine Karimi
# Computational Lexicology & Terminology Lab
# Vrije Universiteit Amsterdam
# Robot Presenter Jelle Brandt Corstius

import spacy
import json
import sys
import os
import IPython
#from ipywidgets import widgets
#from IPython.display import display

nlp = spacy.load('en')   

#Create the input the pipeline will proces
json_schema = 'sample_input.json'
text_from_demo = ''

#def demo_text():
#    global text_widget
#    text_widget = widgets.Text()
#    display(text_widget)
#    def handle_submit(sender):
#        print(text_widget.value)        
#    text_widget.on_submit(handle_submit)
#demo_text()

#print(text_widget.value)

#FUNCTION A: creates a text input from an argument which has to be typed in the following form:
#################  "Hello, this is a new sentence. And this is a newer one"
def choose_text_input():
    global text_for_pipeline
    text_from_commandline = str(sys.argv[1:])
    if "-f" in text_from_commandline:
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
    with open(json_schema, 'r+') as robot_metadata:
        received_data = json.load(robot_metadata)
        text_from_json = received_data["metadata"]["input_text"]
        if text_from_json != 'None':
            received_data["metadata"]["input_text"] = text_for_pipeline
            text_for_spacy = received_data["metadata"]["input_text"]
            robot_metadata.seek(0)
            robot_metadata.write(json.dumps(received_data))
            robot_metadata.truncate()
            print('Dit is de text voor SpaCy', text_for_spacy)

#PROCESSING SEQUENCE 1: Execute all the functions
choose_text_input()
read_json_metadata()

#Process the text with the SpaCy Pipeline 
doc = nlp(text_for_spacy)  
print(doc.text)

#class Semantic():
#    def keywords
#        def keywords
#        def organisations
#        def people
#        def places
#        def topics
#class Emotion():
#   def detect_emotion
#    def information_state
#class Structure
#    "structure": {
#        "prepositional_phrases_count": {
#        "adjective_count": {
#        "non_future": {
 #       "active_sentences": {
  #      "personal_pronouns": {
   #     "word_length": {
    #    "negations": {
     #   "adverbs": {
      #  "passive_sentences": {
      #  "number_of_sentences": {
      #  "future": {
      #  "wordcount": {