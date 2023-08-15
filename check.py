import os
import hashlib
import time

import requests
import json


class FileHashUtil:
    @staticmethod
    def calculate_hash(filename):
        hasher = hashlib.md5()
        with open(filename, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()

    @staticmethod
    def scan_directory(directory):
        file_hashes = {}
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file in ['client_update.exe', 'server_update.exe']:
                    continue
                file_path = os.path.join(root, file)
                file_hash = FileHashUtil.calculate_hash(file_path)
                file_path = file_path.replace('\\', '/')
                file_path = file_path.replace(directory, '', 1)
                file_hashes[file_path] = file_hash
                print(f'file:{file_path},hash:{file_hash}')
        return file_hashes
