from flask import Flask, request, abort, render_template
import server

application = Flask(__name__)

@application.route('/', methods=['GET', 'POST'])
def index():
    if request.method != 'POST':
        abort(501)

@application.route('/hello', methods=['GET'])
def hello():
    return "Hello World!"

@application.route('/annotate/<payload>', methods=['GET'])
def annotate(payload):
    response = server.annotate_and_respond(payload)
    return response

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0')