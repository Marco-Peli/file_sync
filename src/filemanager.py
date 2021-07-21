import hashlib
import json
import os
import time
from _thread import *
from exceptions import *
import os.path


def calc_sha256_chk(data):
    sha256_hash = hashlib.sha256()
    arr = bytearray(data)
    sha256_hash.update(arr)
    hex_hash = sha256_hash.hexdigest()
    return hex_hash


class FileManager:
    def __init__(self, server_req_out):
        self.sync_folder_path = 'files_sync'
        self.files_chk_db = 'files_chk_db.json'
        self.create_files_db()
        self.files_database = self.read_db_file()
        self.incoming_actions = []
        self.server_req_out = server_req_out

    def read_file(self, file_name):
        file_path = self.sync_folder_path + os.sep + file_name
        with open(file_path, "rb") as f:
            return f.read()

    def create_files_db(self):
        database_obj = {
            'files': self.get_folder_content()
        }
        if not os.path.isfile(self.files_chk_db):
            with open(self.files_chk_db, 'w') as db_file:
                json_object = json.dumps(database_obj, indent=2)
                db_file.write(json_object)

    def update_db(self, data):
        database_obj = {
            'files': data
        }
        with open(self.files_chk_db, 'w') as db_file:
            json_object = json.dumps(data, indent=2)
            db_file.write(json_object)

    def read_db_file(self):
        with open(self.files_chk_db, 'r') as db_file:
            return json.load(db_file)

    def start_polling_scan(self):
        start_new_thread(self.scan_files_for_modifies, ())

    def scan_files_for_modifies(self):
        while True:
            files_list = self.get_folder_content()
            db_files_list = self.files_database['files']
            modifies = []
            update_db_file = False

            for file in files_list:
                file_name = file['file_name']
                file_path = self.sync_folder_path + os.sep + file_name
                file_chk = calc_sha256_chk(self.read_file(file_name))
                try:
                    self.find_file_ind_db(file_name) #check if hew file added
                    self.check_db_chk(file_name) #check if file modified by content
                except FileNotFoundInDb:
                    print("New file found, synchronizing new " + file_name)
                    action = {
                        'file_name': file_name,
                        'action': 'new_file',
                        'file_chk': file_chk,
                        'data': file
                    }

                    new_file_data = {
                        'file_name': file_name,
                        'file_chk': file_chk
                    }
                    update_db_file = True
                    db_files_list.append(new_file_data)
                    modifies.append(action)
                except ChkChanged:
                    print("File " + file_name + " has been modified, updating")
                    file = self.read_file(file_name)
                    action = {
                        'file_name': file_name,
                        'action': 'update',
                        'data': self.read_file(file_name)
                    }
                    modifies.append(action)

            if self.check_files_in_folder(db_files_list, modifies): #check if file was deleted
                update_db_file = True

            if self.parse_incoming_req():
                update_db_file = True

            if update_db_file:
                self.update_db(db_files_list)

            time.sleep(3)

    def parse_incoming_req(self):
        pass

    def check_files_in_folder(self, db_files_list, modifies):
        update_db_file = False
        db_files_list = self.files_database['files']

        for file in db_files_list:
            file_name = file['file_name']
            file_path = self.sync_folder_path + os.sep + file_name
            if not os.path.isfile(file_path):
                update_db_file = True
                action = {
                    'file_name': file_name,
                    'action': 'delete',
                }
                db_files_list[:] = list(filter(lambda i: i['file_name'] != file_name, db_files_list))
                modifies.append(action)

        return update_db_file

    def check_db_chk(self, file_name):
        db_files_list = self.files_database['files']
        file_chk = calc_sha256_chk(self.read_file(file_name))
        for file in db_files_list:
            if file_name == file['file_name']:
                if file_chk != file['file_chk']:
                    raise ChkChanged("File chk changed")
        return True

    def find_file_ind_db(self, file_name):
        db_files_list = self.files_database['files']

        for file in db_files_list:
            if file_name == file['file_name']:
                return True

        raise FileNotFoundInDb("file not found in db")

    def add_incoming_req(self, requests):
        self.incoming_actions.append(requests)

    def get_folder_content(self):
        sync_files = os.listdir(self.sync_folder_path)
        files_list = []

        for file_name in sync_files:
            file_path = self.sync_folder_path + os.sep + file_name

            list_obj = {
                'file_name': file_name,
                'file_chk': calc_sha256_chk(self.read_file(file_name))
            }

            files_list.append(list_obj)

        return files_list
