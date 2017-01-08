import json
import os
import spacy
from random import randint

from modules import dbpedia as dbpedia_mod
from modules import emotion as emotion_mod
from modules import response as response_mod
from modules import structure as structure_mod

# A small warning that it may take a while for the data to load
print('------------\nLoading the language model, this may take a while\n\n-------------\n')

# Make sure the spacy module is loaded (this may take a while)
nlp = spacy.load('en')

#PROCESSING PIPELINE: Execute all defined functions and modules:
def annotate_and_respond(text):
    counter = str(randint(0,100))
    outputfile_name = 'processed/processed_sentence_' + counter + '.json'
    outputfile = open(outputfile_name, 'w')
    with open('metadata.json', 'r+') as robot_metadata:
        received_data = json.load(robot_metadata)
        doc = nlp(text)
        dbpedia_mod.semantic_processing_with_dpbedia(doc, received_data, outputfile)
        dict_of_words = structure_mod.create_dict_of_words_vs_postags(doc)
        structure_mod.structural_processor(dict_of_words, doc, received_data, outputfile)
        processed_emotion = emotion_mod.emotion_processor(doc)
        emotion_mod.emotions_extraction(processed_emotion, received_data, outputfile)
        generated_response = response_mod.generate_response(received_data['semantic'])
        received_data['response'] = generated_response
        print(received_data)
        print(generated_response)
        os.system("say " + generated_response)
        outputfile.write(json.dumps(received_data, sort_keys = True, indent=4))
        outputfile.close()
    return generated_response