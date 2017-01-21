#!/usr/bin/python

# This script is meant to demo the VPRO robot conversation
# It is very basic and starts a prompt in which a user can type some text
# This text is enriched with semantic information after which a suitable response or
# set of responses is returned

# Author: Marieke.van.Erp@vu.nl
# Date: 9 December 2016

import json

from modules import emotion as emotion_mod
from modules import response as response_mod


# Run the whole thing
if __name__ == "__main__":
    with open('temp/episode_logfile.json', 'r+') as input:
        data = json.load(input)

        #grab the id of the first throughput "e01_s01_D170116_T110614"
        for tag in data:
            id = tag
            break

        #set the current conversation data to 'received_data', the tag that you will most likely be using in the pipeline
        received_data = data[id]

        #Grabs the emotion and emoratio
        emotion,emoratio = emotion_mod.emotion_ratio(received_data['emotions']['detected_emotion'], 16)
        print ("Emotion found: {} with an emotion ratio of {}".format(emotion,emoratio))

        generated_response = response_mod.generate_response(received_data['semantic'], emotion, emoratio)
        print("Response from pepper: {}".format(generated_response))
    #start()