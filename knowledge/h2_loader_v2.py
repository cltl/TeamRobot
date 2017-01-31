
# coding: utf-8

# In[10]:

import json
import sys
import glob
import random as rand


# In[11]:

light_f, dark_f, non_f = open('knowledge/dbpedia_res/light.json', 'r+', encoding='utf-8'), open('knowledge/dbpedia_res/dark.json', 'r+', encoding='utf-8'), open('knowledge/dbpedia_res/non.json', 'r+', encoding='utf-8')
light, dark, non = json.load(light_f), json.load(dark_f), json.load(non_f)
light_ents, dark_ents, non_ents = light['instance'], dark['instance'], non['instance']
len(light_ents), len(non_ents), len(dark_ents)
hotlist2 = []


# In[12]:

type_file = open('knowledge/dbpedia_res/list_of_types.txt','r+')
typestrings = type_file.readlines()
types = []
for light_type in typestrings:
    types.append(light_type.strip('\n'))


# In[13]:

list_selected_light_entities = []
for light_entity in light_ents:
    for type_url in light_entity['types']:
        type_ = type_url.split('/')[-1]
        for typename in types:
            if typename == type_:
                list_selected_light_entities.append(light_entity)


# In[14]:

list_selected_dark_entities = []
for dark_entity in dark_ents:
    d = dark_entity['uri']
    for statistics in dark_entity['projects']:
        mentions, sources = statistics['mentions'], statistics['sources']
        #print(d, mentions, sources)


# In[15]:

list_non_entities = []
for non_entity in non_ents:
    for statistic in non_entity['projects']:
        mention_count = int(statistic['mentions'])
        if  mention_count > 200:
            list_non_entities.append(non_entity)


# In[18]:
hotlist2 = list_selected_light_entities + dark_ents


# In[19]:

# In[ ]:



