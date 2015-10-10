from gevent import monkey
monkey.patch_all()

import time
from threading import Thread
from flask import Flask, render_template, session, request
from flask.ext.socketio import SocketIO, emit, join_room, leave_room, \
    close_room, disconnect

from uuid import uuid4

from game import Game

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None

game = Game()


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('send char', namespace='/test')
def get_message(message):
    data = message['data']
    game.turn(session['id'], data)
    response = data
    if data == ';':
        response = '<br>'
    emit('my response', {'data': response}, broadcast=True)


@socketio.on('connect', namespace='/test')
def connect():
    session['id'] = str(uuid4())
    print(session['id'])
    game.add_player(session['id'])
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect', namespace='/test')
def disconnect():
    game.remove_player(session['id'])
    print('Client disconnected')


if __name__ == '__main__':
    game.start()
    app.debug = True
    socketio.run(app, host = '0.0.0.0')
