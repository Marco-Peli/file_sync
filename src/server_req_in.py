import json
import socket
from _thread import *


class ServerRequestsIn:

    def __init__(self, file_manager):
        self.host = ''
        self.port = 3010
        self.file_manager = file_manager

    def run_requests_tcp(self, conn):
        while True:
            request = conn.recv(1024)
            if not request:
                break
            parsed_req = json.load(request)
            self.file_manager.add_incoming_req(parsed_req)

    def start(self):
        start_new_thread(self.accept_incoming_conns_tcp, ())

    def accept_incoming_conns_tcp(self):
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.host, self.port))
                s.listen()
                conn, address = s.accept()
                start_new_thread(self.run_requests_tcp, (conn,))