from pprint import pprint

import server_tecs as pepper

while(True):
    pepper_text = input('Talk to pepper: ')
    pepper_text = pepper_text.lower()
    result = pepper.annotate_and_respond(pepper_text, detailed=True)
    print('\n=====')
    print('Concept:\n\t{}\n'
          'Concept Type:\n\t{}\n'
          'Emotion:\n\t{}\n'
          'Topic:\n\t{}'
          .format(result['concept'], result['concept_type'], result['emotion'], result['topic']))
    print('Responses:')
    pprint(result['responses'])
    print('=====\n')