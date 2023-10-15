from sanic          import Sanic, Request
from sanic.response import json
from sanic_cors     import CORS

from moonlight  import Moonlight
from uuid       import uuid4

app: Sanic = Sanic('Sunshine-Database')

CORS(app)

databases: dict[int, Moonlight] = {}

@app.route('/', methods = ['POST'])
async def create_database(request: Request) -> "json":
    requestData: dict[str, any] = {
        'name' : request.json.get('name'),
        'path' : request.json.get('path') if(request.json.get('path')[-1] == '/') else request.json.get('path') + '/'
    }

    database_id: int       = int(str(uuid4().int)[:14])
    databases[database_id] = Moonlight(f'{requestData.get("path")}{requestData.get("name")}.json')

    return json({
        'statusCode' : 200,
        'database'   : database_id
    })

@app.route('/push/<database_id>', methods = ['POST'])
async def push_to_database(request: Request, database_id: int) -> "json":
    return json({
        'statusCode' : 200,
        'database'   : database_id,
        'id'         : await databases.get(database_id).push(request.json)
    })