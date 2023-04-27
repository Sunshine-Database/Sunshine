from database import Sunshine

import time

db = Sunshine('./database/test.json')

db.model(
    'name',
    'age',
    'gender',
    'job'
)

# db.push({
#     'name'   : 'Susan',
#     'gender' : 'Female',
#     'age'    : 22,
#     'job'    : 'React-developer',
#     'kjlfsd' : 'asdfsd'
# })

# db.push({
#     'name'   : 'Mark',
#     'gender' : 'Male',
#     'age'    : 25
# })

# db.push({
#     'name'   : '13215',
#     'gender' : 'Female',
#     'age'    : 22,
#     'job'    : 'React-developer',
#     'qa'     : 'test'
# })

# time.sleep(2)

# db.update(db.get({'name' : 'Susan'})['id'],  {'name' : 'Sussy', 'age' : 30})