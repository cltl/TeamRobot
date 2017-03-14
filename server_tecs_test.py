import server_tecs as server

input = 'darwin brundage miles american'
try:
    response = server.annotate_and_respond(input)
except:
    response = "I am sorry, I do not understand"

print("Response is:\n\t{}".format(response))