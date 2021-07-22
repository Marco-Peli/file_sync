import json
import socket
from _thread import *
import socketio


class ServerCom:

    def __init__(self, file_manager):
        self.requests_out = []
        self.host = 'http://localhost'
        self.port = 3005
        self.file_manager = file_manager
        self.sio = socketio.Client()

        @self.sio.event
        def message(data):
            print('I received a message!')

        @self.sio.on('action')
        def on_message(data):
            print('I received a request!')

        @self.sio.on('currentTime')
        def on_message(data):
            print(data)

    def add_requests(self, actions):
        self.requests_out.append(actions)

    def connect(self):
        self.sio.connect(self.host+':'+str(self.port))
