from database import Sunshine


db = Sunshine('./database/test.json')
print(db)

db.push(
    {
        "name"   : "Andrew",
        "gender" : "male",
        "job"    : "solo developer"
    },
)
db.push(
    {
        "name"   : "Susan",
        "gender" : "female",
        "job"    : "fullstack-developer"
    }
)