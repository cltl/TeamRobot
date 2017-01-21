import sys
import os
import json

def start(template):
    with open(template, 'r+') as template_file:
        data = json.load(template_file)

        responses = {}

        responses['ask_confirmation'] = data['ask_confirmation']
        del data['ask_confirmation']
        responses['no_entities'] = data['no_entities']
        del data['no_entities']

        for key,cat_data in data.items():
            responses[cat_data['type']] = cat_data

        for key,response in responses.items():
            outputfile_name = 'questions/' + key.lower() + '.json'
            outputfile = open(outputfile_name, 'w')
            outputfile.write(json.dumps(response, sort_keys = True, indent=4))
            outputfile.close()

# Run the whole thing
if __name__ == "__main__":
    #hacking argv into this. Should be replaced with a good arg library
    template = "questions/template.json"
    if len(sys.argv) > 2:
        if sys.argv[1] == "-t" or sys.argv[1] == "--template":
            template = sys.argv[2]

    print(template)
    if not os.path.exists(template):
        sys.exit('ERROR: File {} was not found!'.format(template))
    start(template)