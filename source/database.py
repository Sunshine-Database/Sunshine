from filelock import FileLock
from pathlib import Path

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
                database_file.write(json.dumps(EMPTY))

class Sunshine:
    def __init__(self, filename: str, id_field: str = 'id') -> None:
        create_database(filename)
        
        self._id_field = id_field
        self.filename  = filename
        self.lock      = FileLock(f'{self.filename}.lock')

