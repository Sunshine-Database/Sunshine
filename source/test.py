from database import Sunshine

import time

db = Sunshine('./database/test.json')

print(db.get({'name' : 'Tim'}))