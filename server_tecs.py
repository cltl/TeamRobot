import json
import time

from modules import emotion as emotion_mod
from modules import response as response_mod
from modules import matcher
import pytagger

from nltk.corpus import stopwords
stopword_list = stopwords.words('english')

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

def emotion_processor(text, meta_dd):
    tags = pytagger.doTag(text)
    meta_dd['emotions']['detected_emotion'] = tags
    return tags

def create_concept_dictionaries(list_of_json_files):
    list_of_dict = []
    for json_file in list_of_json_files:
        jsonfile = open(json_file)
        json_dict = json.load(jsonfile)
        list_of_dict.append(json_dict)
    return list_of_dict

def concept_indexer(source):
    target_index = {}
    for dict_per_category in source:
        for instance in dict_per_category['instance']:
            concept_dict = {}
            instance_type = instance['instance']
            name = instance['uri'].split("/")[-1].lower().replace("_"," ").replace("+"," ")
            labels = []
            for label_caps in instance['labels']:
                labels.append(label_caps.lower())
            types = []
            for type_ in instance['types']:
                types.append(type_.split("/")[-1])
            concept_dict.update({"types":types})
            concept_dict.update({"labels":labels})
            target_index[name] = concept_dict
    return target_index

def term_idf_indexer(list_of_idf_files):
    for idf_file in list_of_idf_files:
        idf_score_data = open(idf_file)
        term_idf_index = {}
        for line in idf_score_data.readlines():
            term_dict = {}
            term,idf_score = line.strip("\n").split("\t")
            #term_dict["term"] = term
            term_dict["idfscore"] = idf_score
            term_dict["category"] = idf_file
            term_idf_index[term] = term_dict
        return term_idf_index

def input_indexer(input_text):
    input_index = {}
    for term in input_text.split(" "):
        if term not in stopwords.words('english'):
            input_index[term] = input_text.split(" ").count(term)
    return input_index

def match_terms(input_index, term_idf_index):
    matched_terms_dict = {}
    for term_input, tf in input_index.items():
        for term_index, attrib in term_idf_index.items():
            if term_input == term_index:
                matched_term = {}
                matched_terms_dict[term_input] = matched_term
                tf_calc, idf_calc = float(tf), float(attrib['idfscore'])
                tf_idf = tf_calc * idf_calc
                matched_term["tf-idf"] = tf_idf
    return matched_terms_dict

def xpath_get(mydict, path):
    elem = mydict
    try:
        for x in path.strip("/").split("/"):
            elem = elem.get(x)
    except:
        pass
    return elem

def define_respons_concept(matched_terms_dic, concept_index):
    tfidf_max = 0
    interesting_concept = ''
    for k,v in matched_terms_dic.items():
        tfidf = v['tf-idf']
        if tfidf > tfidf_max:
            tfidf_max = tfidf
            interesting_concept = k

    types = []
    typesdict = {}
    for concept,attributes in concept_index.items():
        for label in attributes['labels']:
            if interesting_concept == label:
                for type_ in attributes['types']:
                    types.append(type_)
    for type_ in types:
        typesdict[type_] = types.count(type_)
    interesting_type = max(typesdict, key=lambda i: [1])

    type_max = 0
    for k,v in typesdict.items():
        if k == 'Agent':
            continue
        if v > type_max:
            type_max = v
            interesting_type = k
    return interesting_concept, interesting_type


#'---------LOADED-DICTIONARIES-------------------------------------------------------------------'

conversation_log = {}

list_of_idf_files = "match_module/dbpedia_res/idf_light.tsv", "match_module/dbpedia_res/idf_dark.tsv", "match_module/dbpedia_res/idf_non.tsv"
list_of_json_files = ["match_module/dbpedia_res/light.json", "match_module/dbpedia_res/dark.json", "match_module/dbpedia_res/non.json"]


#'---------PIPELINE-RUNNING--------------------------------------------------------------------'

def annotate_and_respond(text, detailed=False):
    global conversation_log
    response = {}

    timestamp_log = time.strftime("D%y%m%d_T%H%M%S")
    metadata, meta_dd = load_json(text)
    emotion_processor(text,meta_dd)

    conversation_log.update({metadata.strip('.json') + "_" + timestamp_log: meta_dd})

    match = matcher.match_text(text)

    if match:
        concept = match['winner']

        for type in match['types']:
            type = type.split('/')[-1]

            # Fix to include more matches in the results
            if type == 'Country':
                type = 'City'
            if type == 'Location':
                type = 'City'
            if type == 'Place':
                type = 'City'
            if type == 'City':
                # suitable type found
                break

            if type == 'Agent':
                type = 'Person'
            if type == 'Scientist':
                type = 'Person'
            if type == 'Person':
                # suitable type found
                break

            if type == 'College':
                type = 'Institution'
            if type == 'EducationalInstitution':
                type = 'Institution'
            if type == 'Organisation':
                type = 'Institution'
            if type == 'Institution':
                #suitable type found
                break
        category_type = type

    with open('memory/e01_s01_inproces.json', 'w+') as scene:
        scene.write(json.dumps(conversation_log, sort_keys=True, indent=4))

    emotion, emoratio = emotion_mod.emotion_ratio(meta_dd['emotions']['detected_emotion'], len(text.split()))

    response['emotion'] = response_mod.generate_response(emotion=emotion, emoratio=emoratio)
    if match:
        response['concept'] = response_mod.generate_response(concept=concept, category=category_type)
        response['mixed'] = response_mod.generate_response(concept=concept, category=category_type, emotion=emotion, emoratio=emoratio)
    else:
        response['concept'] = 'No concept has been detected in the input text.'
        response['mixed'] = 'No concept has been detected in the input text.'

    topic = pytagger.doTag(text=text, lexicon='resources/topic_lexicon.tsv',
                           tags=['art', 'crime', 'humour', 'live', 'love', 'science', 'technology', 'travel'])

    topic = max(topic.keys(), key=(lambda key: topic[key]))

    if detailed:
        output = {}
        output['responses'] = response
        output['emotion'] = emotion
        output['concept'] = concept
        output['concept_type'] = category_type
        output['topic'] = topic
        return output

    return response