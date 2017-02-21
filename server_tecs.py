import json
import time
import subprocess
from random import randint
from modules import emotion as emotion_mod
from modules import response as response_mod
import nltk
from nltk import word_tokenize
from knowledge import h2_loader_v2
from pprint import pprint

#'---------FUNCTIONS-------------------------------------------------------------------------------'

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

def get_terms(text):
    single_words = []
    combined_words = []
    prev_word = None
    grab_next = False

    words = text.split()
    for word in words:
        if prev_word:
            combined_words.append(prev_word + ' ' + word)

        single_words.append(word)
        prev_word = word

   # pprint(single_words)
   # pprint(combined_words)
    return single_words, combined_words

def map_potential_concepts(words):
    potential_concepts = {}
    concept_id = 1
    for potential_concept in words:
        potential_concepts['pcid'+str(concept_id)] = potential_concept
        concept_id += 1
    return potential_concepts

def emotion_processor(text, meta_dd):
    processor = subprocess.Popen(['echo {} | ./emotionStream.sh'.format(text)], stdout=subprocess.PIPE, shell=True)
    processor_output, _ = processor.communicate()
    decoded_output = processor_output.decode()
    emotions_dict = json.loads(decoded_output)['emotion'][0]
    meta_dd['emotions']['detected_emotion'] = emotions_dict
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

def remove_special_chars(text):
    result = text.replace('_', ' ').replace('-', ' ').replace("'", '').replace('+', ' ').lower()
    result = result.split(' (')[0]
    return result

def strict_matching(value1, value2):
    return value1 == value2

def query_hotlist_one(meta_dd, pcid, pot_con, timestamp, hotlist1_dict):

    concept = {}
    for _,paper in hotlist1_dict.items():
        for _, paper in paper.items():
            prvn = paper['authors']
            if len(prvn) == 2:
                name_val = remove_special_chars(str(prvn['name']))
                if strict_matching(pot_con, name_val):
                    try:
                        inst_val = remove_special_chars(str(prvn['institution']))
                    except KeyError:
                        inst_val = 'none'
                    paper_name = str(paper['title'])
                    name_val += "<" + paper_name + ">" + inst_val

                    concept.update({'Author' : name_val})
                inst_val = remove_special_chars(str(prvn['institution']))
                if strict_matching(pot_con, inst_val):
                    concept.update({'Institution' : (str(prvn['institution']))})
            if len(prvn) == 1:
                if 'name' in prvn.keys():
                    name_val = remove_special_chars(str(prvn['name']))
                    if strict_matching(pot_con, name_val):
                        try:
                            inst_val = remove_special_chars(str(prvn['institution']))
                        except KeyError:
                            inst_val = 'none'
                        paper_name = str(paper['title'])
                        name_val += "<" + paper_name + ">" + inst_val

                        concept.update({'Author': name_val})
                if 'institution' in prvn.keys():
                    inst_val = remove_special_chars(str(prvn['institution']))
                    if strict_matching(pot_con, inst_val):
                        concept.update({'Institution' : (str(prvn['institution']))})

    concept_dictionary = {}

    for type_,concept_sf in concept.items():
        concept_dictionary = create_dict_per_concept(type_,concept_sf, timestamp)
        ent_id = "ent"+str(randint(10,99))
        if type_ == "Author":
            meta_dd['semantic']['authors'].update({ent_id:concept_dictionary})
        if type_ == "Institution":
            meta_dd['semantic']['institutions'].update({ent_id:concept_dictionary})

        return pot_con, concept_dictionary


def query_hotlist_two(meta_dd, pcid, pot_con, timestamp, hl2):
    hotlist2 = hl2
    result = False;
    for instance in hotlist2:
        entity_name = instance['uri'].split('/')[-1]
        entity_name = remove_special_chars(entity_name)
        names = entity_name.split()
        names.append(entity_name)

        for name in names:
            if strict_matching(name, pot_con):
                result = True;
                for type_ in instance['types']:
                    if "/Place" in type_:
                        ent_id = "plc" + (str(randint(10, 99)))
                        instance['mention'] = entity_name
                        instance['type'] = "cities"
                        meta_dd['semantic']['cities'].update({ent_id: instance})
                    if "Institution" in type_:
                        ent_id = "ins" + (str(randint(10, 99)))
                        instance['mention'] = entity_name
                        instance['type'] = "institutions"
                        meta_dd['semantic']['institutions'].update({ent_id: instance})
                    if "/Person" in type_:
                        ent_id = "per" + (str(randint(10, 99)))
                        instance['mention'] = entity_name
                        instance['type'] = "authors"
                        meta_dd['semantic']['authors'].update({ent_id: instance})
    return meta_dd, result

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
hl2 = h2_loader_v2.hotlist2
hotlist1 = open("knowledge/hotlist_1.json", "r+", encoding='utf-8')
hotlist1_dict = json.load(hotlist1)

#'---------PIPELINE-RUNNING--------------------------------------------------------------------'

def annotate_and_respond(text):
    global conversation_log
    global hotlist_0_dict

    timestamp_log = time.strftime("D%y%m%d_T%H%M%S")
    metadata, meta_dd = load_json(text)
    single_nouns, combined_nouns = get_terms(text)
    mapped_single_nouns = map_potential_concepts(single_nouns)
    mapped_combined_nouns = map_potential_concepts(combined_nouns)
    emotion_processor(text,meta_dd)
    dictionary_of_concepts = {}

   # pprint(text)

    for pcid, potential_concept in mapped_combined_nouns.items():
        conceptdict1 = query_hotlist_one(meta_dd, pcid, potential_concept, timestamp_log, hotlist1_dict)
        filter_definitive_concepts(conceptdict1, dictionary_of_concepts)
        conceptdict2, hl2_found = query_hotlist_two(meta_dd, pcid, potential_concept, timestamp_log, hl2)
        filter_definitive_concepts(conceptdict2, dictionary_of_concepts)

    if not hl2_found:
        for pcid, potential_concept in mapped_single_nouns.items():
            conceptdict1 = query_hotlist_one(meta_dd, pcid, potential_concept, timestamp_log, hotlist1_dict)
            filter_definitive_concepts(conceptdict1, dictionary_of_concepts)
            conceptdict2 = query_hotlist_two(meta_dd, pcid, potential_concept, timestamp_log, hl2)
            filter_definitive_concepts(conceptdict2, dictionary_of_concepts)


    for conc_id, concept in dictionary_of_concepts.items():
        hotlist_0_dict = update_hotlist_zero(conc_id, concept, hotlist_0_dict)

    with open('knowledge/hotlist_0.json', 'w+') as hotlist_zero:
        hotlist_zero.write(json.dumps(hotlist_0_dict, sort_keys=True, indent=4))

    conversation_log.update({metadata.strip('.json') + "_" + timestamp_log: meta_dd})

    with open('memory/e01_s01_inproces.json', 'w+') as scene:
        scene.write(json.dumps(conversation_log, sort_keys=True, indent=4))

    emotion, emoratio = emotion_mod.emotion_ratio(meta_dd['emotions']['detected_emotion'], len(text.split()))
   # print ("Emotion found: {} with an emotion ratio of {}".format(emotion, emoratio))
    generated_response = response_mod.generate_response(meta_dd['semantic'], emotion, emoratio)
    return generated_response