import random
import json

def select_question_topic(category):
    accepted = {'Person': 'authors', 'City': 'cities', 'Institution': 'institutions'}

    try:
        question_topic = accepted[category]
    except:
        question_topic = None

    return question_topic

def do_load_questions(question_type):
    with open("questions/" + question_type + ".json") as json_file:
        json_data = json.load(json_file)['responses']
    return json_data


def select_nonsense_question(emotion):
    with open("questions/no_entities.json") as json_file:
        json_data = json.load(json_file)
        question = random.choice(json_data['responses'][emotion])['question']
    return question

def select_response(responses, emotion):
    if emotion in responses:
        response_data = responses[emotion]
    else:
        response_data = responses["neutral"]

    return random.choice(response_data)["question"]

def format_response(response, entity):
    return response.replace("<type>", entity)

def generate_response(concept=False, category=False, emotion=False, emoratio=False):
    #fail-safe
    question_text = "Hmm, I did not quite get that"

    if emotion:
        emotion = emotion.lower()

        # Treshold for which to go with a positive/negative emotion
        # TODO: Built in the emotion module
        emotion_treshold = 0.10

        if emoratio < emotion_treshold:
            emotion = "neutral"
    else:
        emotion = "neutral"

    if not concept:
        question_text = select_nonsense_question(emotion)
        return question_text

    try:
        question_type = select_question_topic(category)
        if question_type is None:
            question_text = select_nonsense_question(emotion)
            return question_text

        responses = do_load_questions(question_type)
        response = select_response(responses, emotion)

        question_text = format_response(response, concept)

    #no entities found
    except IndexError:
        question_text = select_nonsense_question(emotion)

    return(question_text)