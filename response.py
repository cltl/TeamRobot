import os.path
import sys
import json

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = 'bb7589df821148478499279715e8c07c'

def get_response(query):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()

    request.lang = 'en'

    request.query = query

    response = request.getresponse()

    result = json.loads(response.read().decode('utf-8'))

    response = (result['result']['fulfillment']['speech'])

    return response