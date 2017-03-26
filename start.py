from flask import Flask, request, abort, render_template, jsonify
from flask_cors import CORS
import server_tecs as server

from flask_socketio import SocketIO, emit
import sqlite3 as lite
from os import listdir
from os.path import isfile, join
import json
from pprint import pprint


application = Flask(__name__)
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'
#application.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(application)

@socketio.on('my event')
def handle_my_custom_event(json):
    emit('message', json)

@socketio.on('connect', namespace='/event')
def test_connect():
    # need visibility of the global thread object
    print('Client connected')

@socketio.on('annotate', namespace='/event')
def annotate_text(text):
    response = server.annotate_and_respond(text, detailed=True)
    # Write response to database
    # TODO: add DB wrapper
    # con = None
    # con = lite.connect('server/log.db')
    # cur = con.cursor()
    # cur.execute("INSERT INTO Messages(Sender, Receiver, Text, Date) VALUES('" + request.sid +"', 'BOT', '" + text + "', datetime('now','localtime'))")
    # cur.execute("INSERT INTO Messages(Sender, Receiver, Text, Date) VALUES('BOT', '" + request.sid +"', '" + response.replace("'", "\"") + "', datetime('now','localtime'))")
    # con.commit()

    socketio.emit('response', response, namespace="/event", room=request.sid)

@application.route('/logs', methods=['GET'])
def info():
    # TODO: add DB wrapper
    # con = None
    # con = lite.connect('server/log.db')
    # cur = con.cursor()
    # cur.execute("SELECT DISTINCT Sender FROM Messages WHERE Sender != 'BOT'")

    # rows = cur.fetchall()

    return render_template('logs.html', users=rows, user_count=len(rows))

@application.route('/logs/<username>')
def show_log(username):
    # TODO: add DB wrapper
    # con = None
    # con = lite.connect('server/log.db')
    # cur = con.cursor()
    # cur.execute("SELECT * FROM Messages WHERE Sender == '"+username+"' OR Receiver == '"+username+"'")

    # msgs = cur.fetchall()
    return render_template('log.html', msgs=msgs, msg_count=len(msgs), username=username)

@application.route('/', methods=['GET', 'POST'])
def index():
    if request.method != 'POST':
        abort(501)

@application.route('/hello', methods=['GET'])
def hello():
    socketio.emit('message', {'data': 42}, namespace="/event")
    socketio.emit('message', {'age': 25}, broadcast=True, namespace="/event")
    return "Hello World!"

@application.route('/annotate/<text>', methods=['GET'])
def annotate_web(text):
    print('Start manual input')
    response = server.annotate_and_respond(text)
    # response = jsonify(response)
    socketio.emit('response', response, broadcast=True, namespace="/event")
    return jsonify(response)

@application.route('/responses', methods=['GET', 'POST'])
def get_responses():
    files = [f for f in listdir('questions') if isfile(join('questions', f))]
    return json.dumps(files)

@application.route('/responses/<file>', methods=['GET'])
def get_response(file):
    with open('questions/'+file, 'r') as json_file:
        print('do nothing')
        json_data = json.load(json_file)
        pprint(json_data)
        return jsonify(json_data)
    return file

@application.route('/responses/<file>', methods=['POST'])
def post_response(file):
    new_data = request.get_json();

    with open('questions/'+file, 'r') as f:
        json_data = json.load(f)

    json_data['responses'] = new_data

    with open('questions/'+file, 'w') as f:
        json.dump(json_data, f, indent=4)

    return 'Success'


if __name__ == '__main__':
    socketio.run(application, host='0.0.0.0', debug=True)
    #application.run(debug=True, host='0.0.0.0')