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


@socketio.on('send char', namespace='/game')
def get_message(message):
    data = message['data']
    error = game.go(session['id'], data)
    emit('error', {'data': error})
    emit('game state', {'data': game.state()}, broadcast=True)


@socketio.on('start', namespace='/game')
def start(message):
    game.start()
    emit('game state', {'data': game.state()}, broadcast=True)

@socketio.on('connect', namespace='/game')
def connect():
    session['id'] = str(uuid4())
    join_room(session['id'])

    print(session['id'])

    game.add_player(session['id'])
    emit('connection', {'data': 'Connected'})
    emit('player id', {'data': game.players[session['id']].player_id})


@socketio.on('disconnect', namespace='/game')
def disconnect():
    game.remove_player(session['id'])
    for sid, player in game.players.items():
        emit('player id', {'data': player.player_id}, room=sid)
    print('Client disconnected')


if __name__ == '__main__':
    app.debug = True
    socketio.run(app, host = '0.0.0.0')
