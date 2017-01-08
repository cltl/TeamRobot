import json
import urllib.parse
import urllib.request
from random import randint


# Create a dictionary to organise the entity links
def create_entity_dict(selected_values):
    dbp_keys = ('name','type','URI','confidence')
    ent_dict = dict(zip(dbp_keys, selected_values))
    ent_id = 'ent'+str(randint(0,100))
    dict_of_defined_entity = {}
    dict_of_defined_entity[ent_id] = ent_dict
    return dict_of_defined_entity

def extract_entity_values(entity):
    try:
        dbp_resrc = entity['Resources']
        for dbp_resrc_dict in dbp_resrc:
            ent_name_in_dbp = dbp_resrc_dict['@surfaceForm']
            ent_type_in_dbp = dbp_resrc_dict['@types']
            ent_uri_in_dbp = dbp_resrc_dict['@URI']
            ent_conf_in_dbp = dbp_resrc_dict['@similarityScore']
    except KeyError:
        ent_name_in_dbp = ''
        ent_type_in_dbp = ''
        ent_uri_in_dbp = ''
        ent_conf_in_dbp = ''
    return (ent_name_in_dbp, ent_type_in_dbp, ent_uri_in_dbp, ent_conf_in_dbp)

def link_to_dbpedia(doc):
    query = doc
    urlPostPrefixSpotlight = "http://spotlight.sztaki.hu:2222/rest/annotate"
    args = urllib.parse.urlencode([("text", query), ("confidence", 0), ("support", 0)]).encode("utf-8")
    request = urllib.request.Request(urlPostPrefixSpotlight, data=args, headers={"Accept": "application/json"})
    response = urllib.request.urlopen(request).read()
    dbpedia_ent_dict = json.loads(response.decode('utf-8'))
    return dbpedia_ent_dict

def semantic_processing_with_dpbedia(doc, received_data, outputfile):
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