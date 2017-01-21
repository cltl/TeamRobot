import random
import json

def select_question_topic(semantic):
    # TODO: put org/people/places within another key in semantic so we can just loop over them
    subjects = {}
    if len(semantic['authors']):
        subjects['authors'] = len(semantic['authors'])
    if len(semantic['cities']):
        subjects['cities'] = len(semantic['cities'])
    if len(semantic['institutions']):
        subjects['institutions'] = len(semantic['institutions'])

    question_topic = random.choice(list(subjects.keys()))
    return question_topic

def do_load_questions(type):
    with open("questions/" + type + ".json") as json_file:
        json_data = json.load(json_file)['responses']
    return json_data


def select_nonsense_question():
    with open("questions/no_entities.json") as json_file:
        json_data = json.load(json_file)
        question = random.choice(json_data['responses'])['question']
    return question

def check_confidence_values():
    return NotImplemented

def do_select_entity(semantic, type):
    values = list(semantic[type].values())
    return random.choice(values)

def select_response(responses, emotion):
    if emotion in responses:
        response_data = responses[emotion]
    else:
        response_data = responses["neutral"]

    return random.choice(response_data)["question"]

def format_response(response, entity):
    result = response.replace("<type>", entity["mention"])
    result += "?"
    return result

def generate_response(semantic, emotion, emoratio):
    question_text = "Hmm, I did not quite get that"
    emotion = emotion.lower()

    # Treshold for which to go with a positive/negative emotion
    # TODO: Built in the emotion module
    emotion_treshold = 0.10

    if emoratio < emotion_treshold:
        emotion = "neutral"

    try:
        question_type = select_question_topic(semantic)
        #Snelle hardcode, hele response selectie +json structuur moet omgebouwd worden
        if question_type is "authors" and emotion is "neutral":
            author = random.choice(list(semantic['authors'].values()))
            rand = random.random()
            if "institution" in author and rand < 0.5:
                question_text = "{} is affiliated with {}, isn't he?".format(author["mention"], author["institution"])
                return question_text
            else:
                question_text = "{} has written {}, right?".format(author["mention"].title(), author["paper"])
                return question_text

        question_entity = do_select_entity(semantic, question_type)
        responses = do_load_questions(question_type)
        response = select_response(responses, emotion)

        question_text = format_response(response, question_entity)

    #no entities found
    except IndexError:
        question_text = select_nonsense_question()

    return(question_text)