from gevent import monkey
monkey.patch_all()

import time
from threading import Thread
from flask import Flask, render_template, session, request
from flask.ext.socketio import SocketIO, emit, join_room, leave_room, \
    close_room, disconnect

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('send char', namespace='/test')
def get_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)


@socketio.on('connect', namespace='/test')
def connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/test')
def disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    app.debug = True
    socketio.run(app, host = '0.0.0.0')
