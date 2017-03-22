import subprocess

def emotions_extraction(target_emo_dict, received_data, outputfile):
    emotions_score_dict_to_process = target_emo_dict
    for emotion in emotions_score_dict_to_process.items():
        received_data['emotions']['detected_emotion'].append(emotion)


def emotion_select(emodict):
    negative_count = 0
    neutral_count = 0
    positive_count = 0

    negative_count = emodict['anger'] + emodict['disgust'] + emodict['fear'] + emodict['sadness']
    neutral_count = emodict['anticipation'] + emodict['surprise']
    positive_count = emodict['joy'] + emodict['trust']

    negative_count /= 2

    if neutral_count > negative_count and neutral_count > positive_count:
        return "Neutral", neutral_count
    elif positive_count > negative_count:
        return "Positive", positive_count
    elif negative_count > positive_count:
        return "Negative", negative_count

    return "Neutral", 0

def emotion_score(score, wordcount):
    if wordcount > 0:
        return (score/wordcount)
    else:
        return (0)

def emotion_ratio(sample, wordcount):
    emotion,score = emotion_select(sample)
    ratio = emotion_score(score, wordcount)
    return emotion,ratio