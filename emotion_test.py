import json
import time
import subprocess
from random import randint
from modules import emotion as emotion_mod
from modules import response as response_mod
import nltk
from nltk import word_tokenize
from pprint import pprint

#'---------FUNCTIONS-------------------------------------------------------------------------------'

def select_text_input():
    text_for_nlp = "I hate and am angry at stupid abandoning fearful ugly ungrateful brundage"
    return text_for_nlp

def load_json(text):
    metadata_ep_sc = "metadata/e_s.json"
    loaded_metadata = open(metadata_ep_sc,'r+')
    meta_dd = json.load(loaded_metadata)
    episode_scene = metadata_ep_sc.strip(".json").split("/")[1]
    meta_dd["metadata"]["episode_id"], meta_dd["metadata"]["scene_id"] = episode_scene.split("_")
    timestamp = time.strftime("%y-%m-%dT%H:%M:%S")
    meta_dd['metadata']['timestamp'] = timestamp
    text_from_json = meta_dd["metadata"]["input_text"]
    if text_from_json != 'None':
        meta_dd["metadata"]["input_text"] = text
    return metadata_ep_sc, meta_dd

def get_exact_concepts(text):
    list_of_words = []
    for word,tag in nltk.pos_tag(word_tokenize(text)):
        if tag == 'NN':
            list_of_words.append(word)
    return(list_of_words)

def map_potential_concepts(list_words):
    potential_concepts = {}
    #TODO: ask about id
    for potential_concept in list_words:
        potential_concepts['pcid'+str(randint(10,99))] = potential_concept
    return potential_concepts

def emotion_processor(text_input, meta_dd):
    sentence = text_input
    emotions_dict = {}
    emotions_score_dict = {}
    proc = subprocess.Popen(['echo {} | ./emotionStream.sh'.format(sentence)], stdout=subprocess.PIPE, shell=True)
    (out, _) = proc.communicate()
    pprint(out.decode())
    emotions = out.decode().split('],')[0].split(":[")[1:][0].strip("{}}]").split(",")
    for emotion in emotions:
        item0, value0 = emotion.split(":")
        item = item0.strip('"')
        value = int(value0.strip('"'))
        emotions_dict[item] = value
    for key, value in emotions_dict.items():
        emotions_score_dict[key] = value
        meta_dd['emotions']['detected_emotion'] = emotions_score_dict
    return emotions_dict

def create_dict_per_concept(type_,conceptmention, timestamp):
    concept_dict = {}
    if type_ == "Author":
        data = conceptmention.split("<")
        conceptmention = data[0]
        data = data[1].split(">")
        concept_dict['paper'] = data[0]
        if data[1] != 'none':
            concept_dict['institution'] = data[1]
    concept_dict['mention'] = conceptmention
    concept_dict['types'] = type_
    concept_dict['dbp_uri'] = ''
    concept_dict['timestamp'] = timestamp
    return concept_dict

def query_hotlist_one(meta_dd, pcid, pot_con, timestamp):
    hotlist1 = open("knowledge/hotlist_1.json", "r+")
    hotlist1_dict = json.load(hotlist1)
    extracted_concept = pot_con
    concept = {}
    for _,paper in hotlist1_dict.items():
        for _, paper in paper.items():
            prvn = paper['authors']
            if len(prvn) == 2:
                name_val = str(prvn['name']).lower()
                if extracted_concept in name_val:
                    try:
                        inst_val = str(prvn['institution']).lower()
                    except KeyError:
                        inst_val = 'none'
                    paper_name = str(paper['title'])
                    name_val += "<" + paper_name + ">" + inst_val
                    print(name_val)

                    concept.update({'Author' : name_val})
                inst_val = str(prvn['institution']).lower()
                if extracted_concept in inst_val:
                    concept.update({'Institution' : (str(prvn['institution']))})
            if len(prvn) == 1:
                if 'name' in prvn.keys():
                    name_val = str(prvn['name']).lower()
                    if extracted_concept in str(prvn['name']):
                        try:
                            inst_val = str(prvn['institution']).lower()
                        except KeyError:
                            inst_val = 'none'
                        paper_name = str(paper['title'])
                        name_val += "<" + paper_name + ">" + inst_val

                        concept.update({'Author': name_val})
                if 'institution' in prvn.keys():
                    inst_val = str(prvn['institution']).lower()
                    if extracted_concept in str(prvn['institution']):
                        concept.update({'Institution' : (str(prvn['institution']))})
    for type_,concept_sf in concept.items():
        concept_dictionary = create_dict_per_concept(type_,concept_sf, timestamp)
        ent_id = "ent"+str(randint(10,99))
        if type_ == "Author":
            meta_dd['semantic']['authors'].update({ent_id:concept_dictionary})
        if type_ == "Institution":
            meta_dd['semantic']['institutions'].update({ent_id:concept_dictionary})
        return extracted_concept, concept_dictionary

def filter_definitive_concepts(concept, dictionary_of_concepts):
    concept_code = "defcon"+str(randint(10,99))
    dictionary_of_concepts.update({concept_code:concept})

def update_hotlist_zero(concept_code, matched_concept, hotlist_0_dict):
    if matched_concept != None:
        hotlist_0_dict.update({concept_code : matched_concept})
    return hotlist_0_dict

#'---------LOADED-DICTIONARIES-------------------------------------------------------------------'

conversation_log = {}
hotlist_0_dict = {}

#'---------PIPELINE-RUNNING--------------------------------------------------------------------'

def annotate_and_respond(text):
    global conversation_log
    global hotlist_0_dict

    timestamp_log = time.strftime("D%y%m%d_T%H%M%S")
    #text = select_text_input()
    metadata, meta_dd = load_json(text)
    list_of_words = get_exact_concepts(text)
    potent_con = map_potential_concepts(list_of_words)
    emotion_processor(text,meta_dd)
    dictionary_of_concepts = {}

    for pcid, potential_concept in potent_con.items():
        #TODO: Ask about returning two variables
        conceptdict = query_hotlist_one(meta_dd, pcid, potential_concept, timestamp_log)
        filter_definitive_concepts(conceptdict, dictionary_of_concepts)
    for conc_id, concept in dictionary_of_concepts.items():
        hotlist_0_dict = update_hotlist_zero(conc_id, concept, hotlist_0_dict)

    with open('knowledge/hotlist_0.json', 'w+') as hotlist_zero:
        hotlist_zero.write(json.dumps(hotlist_0_dict, sort_keys=True, indent=4))
    conversation_log.update({metadata.strip('.json') + "_" + timestamp_log: meta_dd})

    with open('memory/e01_s01_inproces.json', 'w+') as scene:
        scene.write(json.dumps(conversation_log, sort_keys=True, indent=4))

    # Grabs the emotion and emoratio
    pprint(meta_dd['emotions']['detected_emotion'])
    emotion, emoratio = emotion_mod.emotion_ratio(meta_dd['emotions']['detected_emotion'], len(text.split()))
    print ("Emotion found: {} with an emotion ratio of {}".format(emotion, emoratio))
    generated_response = response_mod.generate_response(meta_dd['semantic'], emotion, emoratio)
    return generated_response

def getcmd():
    cmd = input('\nP3PP3R:> ')
    if cmd == 'quit':
        exit(0)
    annotate_and_respond(cmd)

def start():
    print('\n-------')
    getcmd()
    start()


if __name__ == '__main__':
    start()
    #annotate_and_respond(sys.argv[1])
