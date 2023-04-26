from database import Sunshine


db = Sunshine('./database/test.json')
print(db)

print(db.take(count = 1))

print(db.take({'name' : 'Susan'}))
print(db.take({'name' : 'Olga'}))