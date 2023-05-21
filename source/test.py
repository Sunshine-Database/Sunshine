from database import Sunshine

import time

db = Sunshine('./database/test2.json')

# print(db.push({
#     'name'  : 'Andrey',
#     'age'   : 12,
#     'wsgdk' : True
# }))

#print(db.get())

print(db.update(11576543615062, {
    'age' : 25
}))