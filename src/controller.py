from filemanager import *
from server_req_in import *
from servercom import *


class Controller:
    def __init__(self):
        self.server_com = ServerCom(self)
        self.file_manager = FileManager(self)

    def run_app(self):
        self.file_manager.start_polling_scan()
        self.server_com.connect()
        self.server_com.run()

        while True:
            pass
