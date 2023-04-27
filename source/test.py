from database import Sunshine

import time

db = Sunshine('./database/test.json')
print(db)

print(db.push({
    'name'   : 'Susan',
    'gender' : 'Female',
    'age'    : 22,
    'job'    : 'React-developer'
}))

print(db.push({
    'name'   : 'Mark',
    'gender' : 'Male',
    'age'    : 25,
}))

print(db.get({'name' : 'Susan'}))
time.sleep(3)
print(db.delete(db.get({'name' : 'Mark'})[0]['id']))
time.sleep(3)
print(db.drop())