import json
import time
from _thread import *
import socketio


class ServerCom:

    def __init__(self, controller):
        self.requests_out = []
        self.host = '192.168.1.89'
        self.port = 3005
        self.controller = controller
        self.sio = socketio.Client()

        @self.sio.event
        def message(data):
            print('I received a message!')

        @self.sio.on('action')
        def on_message(actions):
            print('Actions received from remote host')
            json_action = json.loads(actions)
            self.controller.file_manager.add_incoming_req(json_action)

        @self.sio.on('currentTime')
        def on_message(data):
            print(data)

        @self.sio.event
        def connect_error(data):
            pass

    def add_requests(self, actions):
        self.requests_out.append(actions)

    def connect(self):
        try:
            self.sio.connect('http://' + self.host+':'+str(self.port))
        except socketio.exceptions.ConnectionError:
            print("Unable to connect to server")

    def run(self):
        start_new_thread(self.send_to_server, ())

    def send_to_server(self):
        while True:
            if len(self.requests_out) > 0:
                json_object = json.dumps(self.requests_out, indent=None)
                self.sio.emit('action', json_object.encode())
                self.requests_out = []
            time.sleep(5)
