from filelock import FileLock

import uuid
import json
import os

EMPTY: dict[str, list] = {
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

    def _get_load_function(self):
        return json.load

    def _get_dump_function(self):
        return json.dump

    def push(self, data_to_push: dict[str, any]) -> int:
        with self.lock:
            with open(self.filename, 'r+', encoding = 'utf-8') as database_file:
                database_data = json.load(database_file)
                try:
                    if set(database_data['data'][0].keys()) == set(data_to_push.keys()).union([self._id_field]):
                        data_to_push = {self._id_field : self._get_id()} | data_to_push 

                        database_data['data'].append(data_to_push)
                        database_file.seek(0)
                        self._get_dump_function()(database_data, database_file, indent = 4, ensure_ascii = False)
                        
                        return data_to_push[self._id_field]
                    
                    else:
                        data_to_push = {self._id_field : self._get_id()} | data_to_push

                        print(database_data['data'])

                        for i in range(len(database_data['data'])):
                            for key in set(data_to_push.keys()).union([self._id_field]) - set(database_data['data'][0].keys()):
                                database_data['data'][i][str(key)] = ''

                        database_data['data'].append(data_to_push)
                        database_file.seek(0)
                        self._get_dump_function()(database_data, database_file, indent = 4, ensure_ascii = False)
                        
                        return data_to_push[self._id_field]

                except IndexError:
                    data_to_push = {self._id_field : self._get_id()} | data_to_push 
                    database_data['data'].append(data_to_push)
                    database_file.seek(0)
                    self._get_dump_function()(database_data, database_file, indent = 4, ensure_ascii = False)

                    return data_to_push[self._id_field]
                
    def take(self, query: dict = '', count: int = 1) -> list[dict[str, any]]:
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

                return result

            else:
                print('Error: do not use query and count queries in one callback')
                
                return [{'' : ''}]
            