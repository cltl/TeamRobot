import server_tecs as server

input = 'darwin brundage miles american'
input = 'i really like alan turing'
# input = 'i really like ed sheeran'
# input = 'hello darwin'
try:
    response = server.annotate_and_respond(input)
except:
    response = "I am sorry, I do not understand"

print("Response is:\n\t{}".format(response))

import modules.matcher as matcher

match = matcher.match_text(input)

print("Match:"
      "\n\tWinner: {}"
      "\n\tTypes: {}".format(
    match['winner'], match['types']
))