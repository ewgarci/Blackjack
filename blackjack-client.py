#!flask/bin/python
# -*- coding: utf-8 -*-

from socketIO_client import SocketIO, BaseNamespace
from blackjack import Player, Table, Role, States, Deck, Hand, Suits, CardValues, suitDict, cardValues  

class TestNamespace(BaseNamespace):

    def on_test_response(self, *args):
        print 'on_test_response: ', args

def on_broadcast_response(*args):
    print 'on_broadcase_response: ', args

def server_response(*args):
    print 'Recieved: ', args

socketIO = SocketIO('localhost', 5000)
test = socketIO.define(TestNamespace, '/test')

test.emit('my broadcast event', {'data': 'Hello!'}, on_broadcast_response)
test.on('my response', server_response)
socketIO.wait()
