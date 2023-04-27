from itertools import groupby
from filelock import FileLock

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
    
    def model(self, *keys: str):
        with self.lock:
            with open(self.filename, 'r+', encoding = 'utf-8') as database_file:
                database_data: dict = json.load(database_file)
                print(database_data['keys'])
                database_data['keys'] = [key for key, _ in groupby(['id'] + [key for key in keys])]
                
                database_file.seek(0)
                database_file.truncate()
                self._get_dump_function()(database_data, database_file, indent = 4, ensure_ascii = False)
                return 0

    def push(self, data_to_push: dict[str, any]):
        with self.lock:
            with open(self.filename, 'r+', encoding = 'utf-8') as database_file:
                database_data: dict = json.load(database_file)
                
    