import subprocess

# Tag emotions (with Piek's emotion tagger)
def emotion_processor(text_input):
    sentence = text_input #"I am very mad and very very angry at the stupid painful losing Barack Obama in Washigngton DC when he was working with Microsoft in Paris."
    modifier_dict = {}
    emotions_dict = {}
    emotions_score_dict = {}
    proc = subprocess.Popen([ 'echo {} | ./emotionStream.sh'.format(sentence)], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    if err:
        print('Error with the emotion processor')
    modif_output = out.decode().split('],')[1]
    modif_label = modif_output.split(":[")[1:]
    modif = modif_label[0]
    modifiers_as_string = modif.strip("{}}]")
    modifiers = modifiers_as_string.split(",")
    for modifier in modifiers:
        item, value = modifier.split(":")
        item = item.strip('"')
        value = int(value.strip('"'))
        modifier_dict[item] = value
    emo_output = out.decode().split('],')[0]
    emo_label = emo_output.split(":[")[1:]
    emo = emo_label[0]
    emo_as_string = emo.strip("{}}]")
    emotions = emo_as_string.split(",")
    for emotion in emotions:
        item, value = emotion.split(":")
        item = item.strip('"')
        value = int(value.strip('"'))
        emotions_dict[item] = value
    for key, value in emotions_dict.items():
        if value != 0:
            emotions_score_dict[key] = value
    return emotions_score_dict

def emotions_extraction(target_emo_dict, received_data, outputfile):
    emotions_score_dict_to_process = target_emo_dict
    for emotion,value in emotions_score_dict_to_process.items():
        received_data['emotions']['detected_emotion'].append(emotion)