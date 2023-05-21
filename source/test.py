from database import Sunshine

import time

db = Sunshine('./database/test2.json')

db.model('name', 'age', 'wsgdk')

print(db.get({'name' : 'Tim'}))
print(db.push({
    'name'  : 'Andrey',
    'age'   : 12,
    'wsgdk' : True
}))