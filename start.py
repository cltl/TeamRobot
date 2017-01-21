from flask import Flask, request, abort, render_template
import server

from flask_socketio import SocketIO, send, emit


application = Flask(__name__)
application.config['SECRET_KEY'] = 'secret!'
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
    # need visibility of the global thread object
    response = server.annotate_and_respond(text)
    socketio.emit('response', response, namespace="/event")

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
    response = server.annotate_and_respond(text)
    socketio.emit('response', response, broadcast=True, namespace="/event")
    return response

if __name__ == '__main__':
    socketio.run(application, host='0.0.0.0', debug=True)
    #application.run(debug=True, host='0.0.0.0')