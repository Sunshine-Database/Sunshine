# Sunshine

![Sunshine Logo](./sources/sunshine.png)

<h2>Lightweight json-database library for Python</h2>

<br>

## Installing database library
```bash
pip install SunshineDB
```

## Class
<h3>Sunshine - database management class. </h3>

<h3>Has the following set of methods: </h3>

```Python
0. push()
1. all()
2. get()
3. update()
4. contains()
5. delete()
6. drop()
7. backup()
```

<br>
<br>

## Creating database
You just need to create an instance of the Sunshine-class, passing the path to the json-file as an argument.

For example,
```Python
from SunshineDB import Sunshine

database: Sunshine = Sunshine('../databases/database.json')
```

<br>

## Methods
<h3>Method examples will be given using the database variable we set. </h3>

## Quick Methods
* ### [0. Sunshine.push](https://github.com/Sunshine-Database/Sunshine#push)
* ### [1. Sunshine.all](https://github.com/Sunshine-Database/Sunshine#all)
* ### [2. Sunshine.get](https://github.com/Sunshine-Database/Sunshine#get)
* ### [3. Sunshine.update](https://github.com/Sunshine-Database/Sunshine#update)
* ### [4. Sunshine.contains](https://github.com/Sunshine-Database/Sunshine#contains)
* ### [5. Sunshine.delete](https://github.com/Sunshine-Database/Sunshine#delete)
* ### [6. Sunshine.drop](https://github.com/Sunshine-Database/Sunshine#drop)
* ### [7. Sunshine.backup](https://github.com/Sunshine-Database/Sunshine#backup)

### push()
Adds an object with the given fields to the database. <br>
Requires one argument:
* data_to_push (__dictionary[string, any]__) - the key-value dictionary to be added to the database.

Returns ID.
<br>

```Python
identifier: int = database.push(
    {
        'name'       : 'Bertram Gilfoyle',
        'job'        : 'Pied Piper Inc.',
        'occupation' : 'Vice President Of Architecture'
    }
)

print(identifier) 
# output >> 22104564398807 
#           ^^^^^^^^^^^^^^
# ID is 14-digit integer
```

### all()
Returns all database objects. <br>
<br>

```Python
data: list[dict[str, any]] = database.all()

print(data)
# output >> 
# [
#   {
#       'id': 22104564398807, 
#       'name': 'Bertram Gilfoyle', 
#       'job': 'Pied Piper Inc.', 
#       'occupation': 'Vice President Of Architecture'
#   }
# ]
```

### get()
Returns a database object using a query, or returns the number of given elements in the first one up to the number specified in the __count__ argument. <br>
Requires two arguments:
* query (__dictionary[string, any]__) - a key-value dictionary that will be used to select elements,
* count (__integer__)                 - the number of requested elements.

You cannot use both arguments together.
<br>

```Python
data: list[dict[str, any]] = database.get(
    query = {
        'job' : 'Pied Piper Inc.'
    }
)

print(data)
# output >> 
# [
#   {
#       'id': 22104564398807, 
#       'name': 'Bertram Gilfoyle', 
#       'job': 'Pied Piper Inc.', 
#       'occupation': 'Vice President Of Architecture'
#   }
# ]

# And the same will be displayed if you call the get-method like this
data: list[dict[str, any]] = database.get(count = 1)
```

### update()
Updates a database object with an __ID__. <br>
Requires two arguments:
* id             (__14-digit integer__)        - numeric identifier,
* data_to_update (__dictionary[string, any]__) - the key-value dictionary that will be updated in the database object.

<br>

```Python
database.update(
    22104564398807, 
    {
        'occupation' : 'Network engineer'
    }
)
# changed to >> 
# [
#   {
#       'id': 22104564398807, 
#       'name': 'Bertram Gilfoyle', 
#       'job': 'Pied Piper Inc.', 
#       'occupation': 'Network engineer'
#   }
# ]
```

### contains()
Checks by query, if an element is contained in the database. <br>
Requires two arguments:
* key   (__string__),
* value (__any__).

These arguments will be searched in the database.
    
Returns boolean.
<br>

```Python
data: bool = database.contains('name', 'Bertram Gilfoyle')
print(data)
# output >> True
#           ^^^^
# contains-method returns boolean

data: bool = database.contains('name', 'Dinesh Chugtai')
print(data)
# output >> False
```

### delete()
Removes the object with the given __ID__ from the database. <br>
Requires one argument:
* id (__14-digit integer__) - numeric identifier,

<br>

```Python
database.delete(22104564398807)

# database-file >>
# {
#   "data": []
# }
```

### drop()
Removes all objects from the database. 

<br>

```Python
database.drop()

# database-file >>
# {
#   "data": []
# }
```

### backup()
Creates a database backup at the given __path__. <br>
Requires one argument:
* path (__string__) - path to the folder where the backup-file will be saved.

<br>

```Python
database.backup('../databases/backups/')
```

<br>
<br>
<br>

## Author
```
     _      _  _               _ _   
  __| | ___| || |   ___  _   _| | |_ 
 / _` |/ _ \ || |_ / _ \| | | | | __|
| (_| |  __/__   _| (_) | |_| | | |_ 
 \__,_|\___|  |_|  \___/ \__,_|_|\__|
```

## __Thank you a lot!__

<br>

## How to reach me
<a href="https://t.me/de4oult">
    <img src="https://img.shields.io/badge/-Telegram-informational?style=for-the-badge&logo=telegram" alt="Telegram Badge" height="30" />
</a>
<img src="https://img.shields.io/badge/-kayra.dist@gmail.com-informational?style=for-the-badge&logo=gmail" alt="Gmail Badge" height="30" />
