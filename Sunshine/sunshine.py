from Sunshine.messages import Message
from filelock          import FileLock
from datetime          import datetime

import shutil
import uuid
import json
import os

EMPTY: dict[str, list] = {
    'data' : []
}

def create_database(filename: str, create_file: bool = True) -> True:
    if filename.endswith('.json'):
        if create_file and not os.path.exists(filename):
            with open(filename, 'w', encoding = 'utf-8') as database_file:
                database_file.write(json.dumps(EMPTY, indent = 4))
    

class Sunshine:
    """
    Class of json-database. 
    Has the following set of methods: push, all, get, update, contains, delete, drop, backup.
    """
    def __init__(self, filename: str, id_field: str = 'id') -> None:
        """
        Requires the path to the database-file.
        """
        create_database(filename)
        
        self.__id_field = id_field
        self.filename   = filename
        self.lock       = FileLock(f'{self.filename}.lock')

    def __get_id(self) -> int:
        return int(str(uuid.uuid4().int)[:14])

    def __cast_id(self, id: int) -> int:
        return int(id)

    def __get_load_function(self):
        return json.load

    def __get_dump_function(self):
        return json.dump
    
    def push(self, data_to_push: dict[str, any]) -> int:
        """
        Adds an object with the given fields to the database.
        Requires one argument:
            data_to_push (dictionary[string, any]) - the key-value dictionary to be added to the database.

        Returns ID.
        """
        with self.lock:
            with open(self.filename, 'r+', encoding = 'utf-8') as database_file:
                database_data: dict = json.load(database_file)

                data_to_push = {self.__id_field : self.__get_id()} | data_to_push
                        
                database_data['data'].append(data_to_push)
                database_file.seek(0)
                self.__get_dump_function()(database_data, database_file, indent = 4, ensure_ascii = False)
                        
                return data_to_push[self.__id_field]

    def all(self) -> list[dict[str, any]]:
        """
        Returns all database objects.
        """
        with self.lock:
            with open(self.filename, 'r', encoding = 'utf-8') as database_file:
                return self.__get_load_function()(database_file)['data']

    def get(self, query: dict[str, any] = {}, count: int = 1) -> list[dict[str, any]]:
        """
        Returns a database object using a query, or returns the number of given elements in the first one up to the number specified in the `count` argument.
        Requires two arguments:
            query (dictionary[string, any]) - a key-value dictionary that will be used to select elements,
            count (integer)                 - the number of requested elements.

        You cannot use both arguments together.
        """
        with self.lock:
            with open(self.filename, 'r', encoding = 'utf-8') as database_file:
                database_data = self.__get_load_function()(database_file)
                if not query:
                    if count <= len(database_data['data']):
                        data = database_data['data'][0: int(count)]
                        return data
                    
                    else:
                        Message('index out of range', 'error')

                elif query and count == 1:
                    result: dict = []
                    with open(self.filename, 'r', encoding = 'utf-8') as database_file:
                        database_data = self.__get_load_function()(database_file)
                        for data in database_data['data']:
                            if all(x in data and data[x] == query[x] for x in query):
                                result.append(data)

                    return result[0] if len(result) == 1 else result

                else:
                    Message('do not use query and counter in one get-query', 'error')

    def update(self, id: int, data_to_update: dict[str, any]) -> None:
        """
        Updates a database object with an ID.
        Requires two arguments:
            id             (14-digit integer)        - numeric identifier,
            data_to_update (dictionary[string, any]) - the key-value dictionary that will be updated in the database object.
        """
        with self.lock:
            with open(self.filename, 'r+', encoding = 'utf-8') as database_file:
                database_data = self.__get_load_function()(database_file)
                result:  list = []
                updated: bool = False

                for data in database_data['data']:
                    if data[self.__id_field] == self.__cast_id(id):
                        data.update(data_to_update)
                        updated = True

                    result.append(data)
                
                if not updated:
                    Message('there is no element with given `id`', 'error')
                
                database_data["data"] = result
                database_file.seek(0)
                database_file.truncate()
                self.__get_dump_function()(database_data, database_file, indent = 4, ensure_ascii = False)

    def contains(self, key: str, value: any) -> bool:
        """
        Checks by query, if an element is contained in the database.
        Requires two arguments:
            key   (string),
            value (any).
        These arguments will be searched in the database.

        Returns boolean.
        """
        return True if self.get(query = {key : value}) != [] else False

    def delete(self, id: int) -> None:
        """
        Removes the object with the given ID from the database.
        Requires one argument:
            id (14-digit integer) - numeric identifier,
        """
        with self.lock:
            with open(self.filename, 'r+', encoding = 'utf-8') as database_file:
                database_data = self.__get_load_function()(database_file)
                result: list = []
                found:  bool = False

                for data in database_data['data']:
                    if data.get(self.__id_field) == self.__cast_id(id):
                        found = True
                    else:
                        result.append(data)

                if not found:
                    Message('there is no element with given `id`', 'error')

                database_data['data'] = result
                database_file.seek(0)
                database_file.truncate()
                self.__get_dump_function()(database_data, database_file, indent = 4, ensure_ascii = False)
    
    def drop(self) -> None:
        """
        Removes all objects from the database.
        """
        with self.lock:
            with open(self.filename, 'w', encoding = 'utf-8') as database_file:
                database_file.write(json.dumps(EMPTY, indent = 4))

    def backup(self, path: str) -> None:
        """
        Creates a database backup at the given path.
        Requires one argument:
            path (string) - path to the folder where the backup-file will be saved.
        """
        if not os.path.exists(path): os.mkdir(path)
        filename: str = self.filename.split('/')[-1] if '/' in self.filename else self.filename
        shutil.copy(self.filename, f'{path}/{datetime.strftime(datetime.now(), "%H:%M:%S.%f-%d-%m-%Y")}-{filename}')