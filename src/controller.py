from filemanager import *
from server_req_in import *
from server_req_out import *


class Controller:
    def __init__(self):
        self.server_req_out = ServerReqOut()
        self.file_manager = FileManager(self.server_req_out)
        self.server_in = ServerRequestsIn(self.file_manager)

    def run_app(self):
        self.file_manager.start_polling_scan()
        self.server_in.start()
        self.server_req_out.run()

        while True:
            pass
