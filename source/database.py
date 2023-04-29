from itertools import groupby
from filelock import FileLock
from datetime import datetime

import shutil
import uuid
import json
import os

EMPTY: dict[str, list] = {
    'keys' : [],
    'data' : []
}

def create_database(filename: str, create_file: bool = True) -> True:
    if filename.endswith('.json'):
        if create_file and not os.path.exists(filename):
            with open(filename, 'w') as database_file:
                database_file.write(json.dumps(EMPTY, indent = 4))
    

class Sunshine:
    def __init__(self, filename: str, id_field: str = 'id') -> None:
        create_database(filename)
        
        self._id_field = id_field
        self.filename  = filename
        self.lock      = FileLock(f'{self.filename}.lock')

    def _get_id(self) -> int:
        return int(str(uuid.uuid4().int)[:18])

    def _cast_id(self, id: int) -> int:
        return int(id)

    def _get_load_function(self):
        return json.load

    def _get_dump_function(self):
        return json.dump
    
    def model(self, *keys: str) -> int:
        with self.lock:
            with open(self.filename, 'r+', encoding = 'utf-8') as database_file:
                database_data: dict = json.load(database_file)
                database_data['keys'] = [key for key, _ in groupby(['id'] + [key for key in keys])]
                
                for key in database_data['keys']:
                    if key not in keys and key != 'id':
                        del database_data['keys'][database_data['keys'].index(key)]
                        
                for key in database_data['keys']:
                    for i in range(len(database_data['data'])):
                        if not database_data['data'][i].get(key):
                            database_data['data'][i][key] = 'empty'

                for i in range(len(database_data['data'])):
                    if set(database_data['data'][i]).symmetric_difference(set(database_data['keys'])):
                        for key in (set(database_data['data'][i]).symmetric_difference(set(database_data['keys']))):
                            del database_data['data'][i][key]

                database_file.seek(0)
                database_file.truncate()
                self._get_dump_function()(database_data, database_file, indent = 4, ensure_ascii = False)              
                return 0

    def push(self, data_to_push: dict[str, any]):
        with self.lock:
            with open(self.filename, 'r+', encoding = 'utf-8') as database_file:
                database_data: dict = json.load(database_file)

                if set(data_to_push).difference(set(database_data['keys'])): raise Exception('Error: no key in model')
                data_to_push = {self._id_field : self._get_id()} | data_to_push
                for key in database_data['keys']:
                    if key in set(data_to_push).symmetric_difference(set(database_data['keys'])):
                        data_to_push[key] = 'empty'
                        
                database_data['data'].append(data_to_push)
                database_file.seek(0)
                self._get_dump_function()(database_data, database_file, indent = 4, ensure_ascii = False)
                        
                return data_to_push[self._id_field]

    def backup(self, path: str) -> int:
        if not os.path.exists(path): os.mkdir(path)
        if '/' in self.filename: filename = self.filename.split('/')[-1]
        shutil.copy(self.filename, f'{path}/{datetime.strftime(datetime.now(), "%H:%M:%S.%f-%d-%m-%Y")}-{filename}')
        return 0
    
    def drop(self) -> None:
        with self.lock:
            with open(self.filename, 'w', encoding = 'utf-8') as database_file:
                database_file.write(json.dumps(EMPTY, indent = 4))