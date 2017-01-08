# Also get the part of speech tags and make sure there is a structure for them
def create_dict_of_words_vs_postags(doc):
    dict_of_words = {}
    for word in doc:
        dict_of_words[word.string] = word.tag_

    return dict_of_words

# Gather stats about the structure of the conversation
def structural_processor(dict_of_words, doc, received_data, outputfile):
    received_data['structure']['wordcount'] = int(len(dict_of_words))
    for sent in doc.sents:
        received_data['structure']['number_of_sentences'] += 1
    for word in doc:
        if 'JJ' in word.tag_:
            received_data['structure']['adjective_count'] += 1
        if 'RB' in word.tag_:
            received_data['structure']['adverbs'] += 1
        if 'PRP' in word.tag_:
            received_data['structure']['personal_pronouns'] += 1
        if 'VBD' in word.tag_:
            received_data['structure']['non_future'] += 1
        if 'VBN' in word.tag_:
            received_data['structure']['non_future'] += 1
        if 'VB' in word.tag_:
            received_data['structure']['future'] += 1
        if 'VBG' in word.tag_:
            received_data['structure']['future'] += 1
        if 'VBP' in word.tag_:
            received_data['structure']['future'] += 1
        if 'VBZ' in word.tag_:
            received_data['structure']['future'] += 1
    for dependency in doc:
        if dependency.dep_ == 'neg':
            received_data['structure']['negations'] += 1
        if dependency.dep_ == 'prep':
            received_data['structure']['prepositional_phrases_count'] += 1
        if dependency.dep_ == 'aux':
            received_data['structure']['active_sentences'] += 1
        if dependency.dep_ == 'auxpass':
            received_data['structure']['passive_sentences'] += 1