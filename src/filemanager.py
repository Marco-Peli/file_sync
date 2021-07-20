import hashlib
import json
import os
import time
from _thread import *
from exceptions import *


def calc_sha256_chk(data):
    sha256_hash = hashlib.sha256()
    arr = bytearray(data)
    sha256_hash.update(arr)
    hex_hash = sha256_hash.hexdigest()
    return hex_hash


class FileManager:
    def __init__(self):
        self.sync_folder_path = 'files_sync'
        self.files_chk_db = 'files_chk_db.json'
        self.create_files_db()
        self.files_database = self.read_db_file()

    def read_file(self, file_name):
        file_path = self.sync_folder_path + os.sep + file_name
        with open(file_path, "rb") as f:
            return f.read()

    def create_files_db(self):
        database_obj = {
            'files': self.get_folder_content()
        }

        with open(self.files_chk_db, 'w') as db_file:
            json_object = json.dumps(database_obj, indent=2)
            db_file.write(json_object)

    def update_db(self, data):
        pass

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

            for file in files_list:
                file_name = file['file_name']
                file_path = self.sync_folder_path + os.sep + file_name
                last_modify = os.path.getmtime(file_path)
                file_chk = calc_sha256_chk(self.read_file(file_name))
                try:
                    self.find_file_ind_db(file_name)
                    self.check_last_modify(file_name)
                    self.check_db_chk(file_name)
                except FileNotFoundInDb:
                    print("New file found, synchronizing new " + file_name)
                    action = {
                        'file_name': file_name,
                        'action': 'update',
                        'data': self.read_file(file_name)
                    }
                    modifies.append(action)
                except LastModifyChanged:
                    print("File " + file_name + " has been modified, updating")
                    action = {
                        'file_name': file_name,
                        'action': 'update',
                        'data': self.read_file(file_name)
                    }
                    modifies.append(action)
                except ChkChanged:
                    print("File " + file_name + " has been modified, updating")
                    action = {
                        'file_name': file_name,
                        'action': 'update',
                        'data': self.read_file(file_name)
                    }
                    modifies.append(action)

            time.sleep(5)

    def check_last_modify(self, file_name):
        file_path = self.sync_folder_path + os.sep + file_name
        file_last_mod = os.path.getmtime(file_path)
        db_files_list = self.files_database['files']

        for file in db_files_list:
            if file_name == file['file_name']:
                if file_last_mod != file['last_modify']:
                    raise LastModifyChanged("Last modify changed")

        return True

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

    def get_folder_content(self):
        sync_files = os.listdir(self.sync_folder_path)
        files_list = []

        for file_name in sync_files:
            file_path = self.sync_folder_path + os.sep + file_name

            list_obj = {
                'file_name': file_name,
                'last_modify': os.path.getmtime(file_path),
                'file_chk': calc_sha256_chk(self.read_file(file_name))
            }

            files_list.append(list_obj)

        return files_list
