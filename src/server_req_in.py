import json


class ServerRequestsIn:

    def __init__(self):
        pass

    def run_requests_tcp(self, conn):
        while True:
            request = conn.recv(1024)
            if not request:
                break
            response = self.server_req_handler.parse_req(request)
            json_object = json.dumps(response, indent=None)
            conn.send(json_object.encode())
        if self.connected_tcp_clients > 0:
            self.connected_tcp_clients -= 1
        if self.connected_tcp_clients == 0:
            self.controller.set_server_status_idle("TCP Server ON, idle")

    def accept_incoming_conns_tcp(self, thread_name):
        """Main server tcp thread that will accept incoming connections

        Args:
        -------
        thread_name : str
            the name of the thread the server lays on
        """
        self.controller.set_server_status_idle("TCP Server ON, idle")
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.host, self.config_obj.config['incoming_req_server_port']))
                s.listen()
                conn, address = s.accept()
                start_new_thread(self.run_requests_tcp, (conn,))