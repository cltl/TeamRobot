import random
import json

def select_question_topic(semantic):
    # put org/people/places within another key in semantic so we can just loop over them
    subjects = {}
    if len(semantic['organisations']):
        subjects['organisations'] = len(semantic['organisations'])
    if len(semantic['people']):
        subjects['people'] = len(semantic['people'])
    if len(semantic['places']):
        subjects['places'] = len(semantic['places'])

    question_topic = random.choice(list(subjects.keys()))
    return question_topic

def select_question_file(topic):
    # use a weight to determine if selecting a general question or a more specific question
    # to even out all odds, put the general questions in each specific topic's question dict
    general_question_weight = 0.7
    if random.random() <= general_question_weight:
        question_file = "general.json"
    else:
        question_file = topic + ".json"

    return question_file

def select_question(file):
    # load questions and select one at random. Only have one variable for now so select from x
    # With multiple parameters we can add x_y, x_y_z, etc.
    with open("questions/" + file) as json_file:
        json_data = json.load(json_file)
        question = random.choice(json_data['x'])['question']
    return question

def generate_response(semantic):
    try: 
        question_topic = select_question_topic(semantic)
        question_subject = random.choice(list(semantic[question_topic].values()))
        question_file = select_question_file(question_topic)
        question_text = select_question(question_file).replace('{x}', question_subject['name'])
    except:
        question_text = """Nice weather today, is it not?""" 
    return(question_text)