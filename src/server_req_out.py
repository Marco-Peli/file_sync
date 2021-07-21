import socket
from _thread import *


class ServerReqOut:

    def __init__(self):
        self.requests_out = []
        self.host = '127.0.0.1'
        self.port = 3010

    def add_requests(self, actions):
        self.requests_out.append(actions)

    def run(self):
        start_new_thread(self.dispatch_requests, ())

    def dispatch_requests(self):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if len(self.requests_out) > 0:
                    s.connect((self.host, self.port))
                    s.send(bytes(self.requests_out))
