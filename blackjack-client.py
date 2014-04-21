#!flask/bin/python
# -*- coding: utf-8 -*-

from socketIO_client import SocketIO, BaseNamespace
from blackjack import Player, Table, Role, States, Deck, Hand, Suits, CardValues, suitDict, cardValues  
import threading
import sys,struct,fcntl,termios
import time,readline,thread


def blank_current_readline():
# Next line said to be reasonably portable for various Unixes
    (rows,cols) = struct.unpack('hh', fcntl.ioctl(sys.stdout,
    termios.TIOCGWINSZ,'1234'))

    text_len = len(readline.get_line_buffer())+2

    # ANSI escape sequences (All VT100 except ESC[0G)
    # Clear current line
    sys.stdout.write('\x1b[2K')
    # Move cursor up and clear line
    sys.stdout.write('\x1b[1A\x1b[2K'*(text_len/cols))
    # Move to start of line
    sys.stdout.write('\x1b[0G')

def noisy_thread():
    while True:
        time.sleep(3)
        blank_current_readline()
        print 'Interrupting text!'
        sys.stdout.write('> ' + readline.get_line_buffer())
        # Needed or text doesn't show until a key is pressed
        sys.stdout.flush()



class TestNamespace(BaseNamespace):

    def on_test_response(self, *args):
        print 'on_test_response: ', args

def on_broadcast_response(*args):
    print 'on_broadcase_response: ', args

def server_state(*args):
    blank_current_readline()
    print 'Current game state: ' + args['state']
    sys.stdout.write(':> ' + readline.get_line_buffer())
    # Needed or text doesn't show until a key is pressed
    sys.stdout.flush()

def server_response(*args):
    blank_current_readline()
    print 'Recieved: ', args
    sys.stdout.write(':> ' + readline.get_line_buffer())
    # Needed or text doesn't show until a key is pressed
    sys.stdout.flush()

def process():
#     name = "user"
#     msg = "default"
#     while True:
#         name = raw_input("What is your name? ").strip()
#         if name == "":
#             print "Invalid Name"
#         else:
#             test.emit('login', {'data': msg, 'user': name})
#             break
# 
#     while True:
#         #msg = raw_input(name + ":> ").strip()
#         msg = raw_input(":> ")
#         if name == "":
#             print "Invalid Msg"
#         else:
#             #test.emit('my broadcast event', {'data': msg, 'user': name})
#             test.emit('my event', {'data': msg, 'user': name})
    socketIO.wait()

cmds2events = {
    'bet':'bet',
    'stand':'stand',
    'msg':'msg',
    'hit':'hit'
}

if __name__ == '__main__':
#     thread.start_new_thread(noisy_thread, ())
#     while True:
#         s = raw_input('> ')
    socketIO = SocketIO('localhost', 5000)
    test = socketIO.define(TestNamespace, '/test')
    test.on('serverResponse', server_response)
    test.on('serverState', server_state)
#socketIO.wait()
#    thread.start_new_thread(process, ())
#    thread = threading.Thread(target=process)
#    thread.start()
#    socketIO.wait()

    name = "user"
    cmdLine = ""
    while True:
        name = raw_input("What is your name? ").strip()
        if name == "":
            print "Invalid Name"
        else:
            test.emit('login', {'user': name})
            break

    while True:
        #msg = raw_input(name + ":> ").strip()
        cmdLine = raw_input(":> ")
        if cmdLine == "":
            print "Invalid command"
        else:
            tokens = cmdLine.lower().split()
            event = cmds2events.get(tokens[0], None)

            if event is None:
                print "Invalid command"
            elif tokens[0] == 'bet' and len(tokens) == 2:
                try:
                    amount = int(tokens[1])
                except ValueError:
                    print "Invalid bet amount"
                else:
                    test.emit(event, {'bet': amount, 'user': name})
            elif tokens[0] == 'msg' and len(tokens) > 1:
                msg = ' '.join(tokens[1:])
                test.emit('my broadcast event', {'data': msg, 'user': name})
            else:
                print "Invalid command"

            #test.emit('my broadcast event', {'data': msg, 'user': name})
            #test.emit('my event', {'data': msg, 'user': name})

