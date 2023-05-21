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
        return int(str(uuid.uuid4().int)[:14])

    def _cast_id(self, id: int) -> int:
        return int(id)

    def _get_load_function(self):
        return json.load

    def _get_dump_function(self):
        return json.dump
    
    def push(self, data_to_push: dict[str, any]):
        with self.lock:
            with open(self.filename, 'r+', encoding = 'utf-8') as database_file:
                database_data: dict = json.load(database_file)

                data_to_push = {self._id_field : self._get_id()} | data_to_push
                        
                database_data['data'].append(data_to_push)
                database_file.seek(0)
                self._get_dump_function()(database_data, database_file, indent = 4, ensure_ascii = False)
                        
                return data_to_push[self._id_field]

    def get(self, query: dict[str, any] = {}, count: int = 1) -> list[dict[str, any]]:
        with self.lock:
            with open(self.filename, 'r', encoding = 'utf-8') as database_file:
                database_data = self._get_load_function()(database_file)
                if not query:
                    if count <= len(database_data['data']):
                        data = database_data['data'][0: int(count)]
                        return data
                    
                    else:
                        print('Out of range')

                elif query and count == 1:
                    result: dict = []
                    with open(self.filename, 'r', encoding = 'utf-8') as database_file:
                        database_data = self._get_load_function()(database_file)
                        for data in database_data['data']:
                            if all(x in data and data[x] == query[x] for x in query):
                                result.append(data)

                    return result[0] if len(result) == 1 else result

                else:
                    raise Exception('Error: do not use query and count queries in one request')

    def update(self, id: int, data_to_update: dict[str, any]) -> int:
        with self.lock:
            with open(self.filename, 'r+', encoding = 'utf-8') as database_file:
                database_data = self._get_load_function()(database_file)
                result:  list = []
                updated: bool = False

                for data in database_data['data']:
                    if data[self._id_field] == self._cast_id(id):
                        data.update(data_to_update)
                        updated = True

                    result.append(data)
                
                if not updated:
                    raise Exception('Error: there is no element with given `id`')
                
                database_data["data"] = result
                database_file.seek(0)
                database_file.truncate()
                self._get_dump_function()(database_data, database_file, indent = 4, ensure_ascii = False)

        return 0

    def delete(self, id: int) -> int:
        with self.lock:
            with open(self.filename, 'r+', encoding = 'utf-8') as database_file:
                database_data = self._get_load_function()(database_file)
                result: list = []
                found:  bool = False

                for data in database_data['data']:
                    if data.get(self._id_field) == self._cast_id(id):
                        found = True
                    else:
                        result.append(data)

                if not found:
                    raise Exception('Error: there is no element with given `id`')

                database_data['data'] = result
                database_file.seek(0)
                database_file.truncate()
                self._get_dump_function()(database_data, database_file, indent = 4, ensure_ascii = False)

        return 0

    def backup(self, path: str) -> int:
        if not os.path.exists(path): os.mkdir(path)
        if '/' in self.filename: filename = self.filename.split('/')[-1]
        shutil.copy(self.filename, f'{path}/{datetime.strftime(datetime.now(), "%H:%M:%S.%f-%d-%m-%Y")}-{filename}')
        return 0
    
    def drop(self) -> None:
        with self.lock:
            with open(self.filename, 'w', encoding = 'utf-8') as database_file:
                database_file.write(json.dumps(EMPTY, indent = 4))