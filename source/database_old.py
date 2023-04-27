from filelock import FileLock

import uuid
import json
import os

EMPTY: dict[str, list] = {
    "keys" : [],
    "data" : []
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

    def push(self, data_to_push: dict[str, any]) -> int:
        with self.lock:
            with open(self.filename, 'r+', encoding = 'utf-8') as database_file:
                database_data: dict = json.load(database_file)
                try:
                    if set(database_data['data'][0].keys()) == set(data_to_push.keys()).union([self._id_field]):
                        print(set(data_to_push.keys()) - set(database_data['keys']))
                        database_data['keys'].append(set(data_to_push.keys()).difference(set(database_data['keys'])))

                        data_to_push = {self._id_field : self._get_id()} | data_to_push 

                        database_data['data'].append(data_to_push)
                        database_file.seek(0)
                        self._get_dump_function()(database_data, database_file, indent = 4, ensure_ascii = False)
                        
                        return data_to_push[self._id_field]
                    
                    else:
                        data_to_push = {self._id_field : self._get_id()} | data_to_push

                        for i in range(len(database_data['data'])):
                            print(database_data['data'][i])
                            for key in set(data_to_push.keys()).union([self._id_field]) - set(database_data['data'][0].keys()):
                                database_data['data'][i][str(key)] = ''
                                print(data_to_push)
                                
                        database_data['data'].append(data_to_push)
                        database_file.seek(0)
                        self._get_dump_function()(database_data, database_file, indent = 4, ensure_ascii = False)
                            
                        return data_to_push[self._id_field]

                except IndexError:
                    for key in data_to_push:
                        database_data['keys'].append(key)

                    data_to_push = {self._id_field : self._get_id()} | data_to_push 
                    database_data['data'].append(data_to_push)
                    database_file.seek(0)
                    self._get_dump_function()(database_data, database_file, indent = 4, ensure_ascii = False)

                    return data_to_push[self._id_field]
                
    def get(self, query: dict = {}, count: int = 1) -> list[dict[str, any]]:
        with self.lock:
            if not query:
                try:
                    with open(self.filename, 'r', encoding = 'utf-8') as database_file:
                        database_data = self._get_load_function()(database_file)
                    
                    if count <= len(database_data['data']):
                        data = database_data['data'][0: int(count)]
                        return data
                    
                    else:
                        print('Error: out of range') # raise LengthError
                
                except:
                    return [{'' : ''}]
            
            elif query and count == 1:
                result = []
                with open(self.filename, 'r', encoding = 'utf-8') as database_file:
                    database_data = self._get_load_function()(database_file)
                    for data in database_data['data']:
                        if all(x in data and data[x] == query[x] for x in query):
                            result.append(data)

                return result[0]

            else:
                print('Error: do not use query and count queries in one callback')
                
                return [{'' : ''}]
        
    def update(self, id: int, data_to_update: dict[str, any]) -> None:
        updated: bool = False
        
        with self.lock:
            with open(self.filename, 'r+', encoding = 'utf-8') as database_file:
                database_data: dict = self._get_load_function()(database_file)
                result: list = []
    
                if set(data_to_update.keys()).issubset(database_data['data'][0].keys()):
                    for data in database_data['data']:
                        if data[self._id_field] == self._cast_id(id):
                            data.update(data_to_update)
                            updated = True

                        result.append(data)

                    if not updated:
                        print('error: not updated') # raise Error
                        exit()

                    database_data['data'] = result
                    database_file.seek(0)
                    database_file.truncate()
                    self._get_dump_function()(database_data, database_file, indent = 4, ensure_ascii = False)

                    return 200

                else:
                    print('schema error')

    def delete(self, id: int = 0) -> bool:
        with self.lock:
            with open(self.filename, 'r+', encoding = 'utf-8') as database_file:
                database_data: dict = self._get_load_function()(database_file)
                result: list = []
                found: bool  = False

                for data in database_data['data']:
                    if data[self._id_field] == self._cast_id(id):
                        found = True
                    else:
                        result.append(data)

                if not found:
                    pass # raise IdNotFoundError

                database_data['data'] = result
                database_file.seek(0)
                database_file.truncate()
                self._get_dump_function()(database_data, database_file, indent = 4, ensure_ascii = False)

            return True
        
    def drop(self) -> None:
        with self.lock:
            with open(self.filename, 'w', encoding = 'utf-8') as database_file:
                database_file.write(json.dumps(EMPTY, indent = 4))