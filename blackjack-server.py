#!flask/bin/python
# -*- coding: utf-8 -*-

import time
from threading import Thread
from flask import Flask, render_template, session, request
from flask.ext.socketio import SocketIO, emit, join_room, leave_room
from blackjack import Player, Table, Role, States, Deck, Hand, Suits, CardValues, suitDict, cardValues  

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'Awesome Sauce!'
socketio = SocketIO(app)
table = Table()
deck = Deck(8)

def background_thread():
    """Main game loop"""
    while True:
        if table.state == States.BETTING and len(table.players) > 0:
#             emit('serverState',
#                     {'state': table.state},  broadcast=True)
            emit('serverResponse',
                    {'data': "10 seconds to place bets for round " + str(table.roundNumber), 'round': table.roundNumber},  broadcast=True)
            time.sleep(10)
            if len(table.activePlayer) > 0:
                table.state == States.DEALING
                table.roundNumber +=1
#                 emit('serverState',
#                     {'state': table.state},  broadcast=True)
            else:
                emit('serverResponse',
                    {'data': "No bets made, restarting round" + str(table.roundNumber), 'round': table.roundNumber},  broadcast=True)
        if table.state == States.DEALING:
            emit('serverResponse',
                    {'data': "2 seconds to deal", 'round': table.roundNumber},  broadcast=True)
            time.sleep(2)
            table.state == States.BETTING
        time.sleep(5)




@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('serverResponse',
         {'data': message['data'], 'count': session['receive_count']})

@socketio.on('my event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('serverResponse',
         {'data': message['data'], 'count': session['receive_count']})

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('serverResponse',
        {'data': message['data'], 'count': session['receive_count'], 'user': message.get('user', 'Anonymous')}, broadcast=True)

@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('serverResponse',
         {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
          'count': session['receive_count']})

@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('serverResponse',
         {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
          'count': session['receive_count']})

@socketio.on('my room event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('serverResponse',
        {'data': message['data'], 'count': session['receive_count']},
        room=message['room'])

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('serverResponse', {'data': 'Connected', 'count': 0})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

@socketio.on('login', namespace='/test')
def login_player(message):
    if 'user' in message: 
        newPlayer = Player(100, message['user'], Role.HUMAN)
        table.players.append(newPlayer)
        emit('serverResponse',
            {'data': message['user'] + ' joined the table'}, broadcast=True)
    else: 
        emit('serverResponse',
            {'data': 'Invalid login'})

@socketio.on('joinTable', namespace='/test')
def join_table(message):
    if 'user' in message: 
        newPlayer = Player(100, message['user'], Role.HUMAN)
        table.players.append(newPlayer)
    else: 
        emit('serverResponse',
            {'data': 'Invalid login'})

@socketio.on('bet', namespace='/test')
def place_bet(message):
    if 'user' in message and 'bet' in message: 
        p = getPlayer(message['user'])
        if p is None:
            emit('serverResponse', {'data': 'User not found'})
        elif message['bet'] > p.purse:
            emit('serverResponse', {'data': 'Insufficient Funds'})
        elif message['bet'] == 0:
            p.bet = message['bet']
            emit('serverResponse', {'data': 'Sitting Out'}, broadcast=True)
        elif message['bet'] > 0:
            p.bet = message['bet']
            emit('serverResponse', {'data': p.name + ': betting ' + str(p.bet)}, broadcast=True)
            table.activePlayers.append(p)
        else:
            emit('serverResponse', {'data': 'Invalid Command'})
    else: 
        emit('serverResponse', {'data': 'Invalid Command'})

if __name__ == '__main__':
    Thread(target=background_thread).start()
    socketio.run(app)
