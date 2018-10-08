import json
from flask import Flask, Response, request

# CONSTANTS
ID_ERROR = 'ID does not exist'
SUCCESSFUL_CODE = 200

# SIMPLE DATABASE EXAMPLE
SIMPLE_STORAGE = {}
SIMPLE_ID = 0

app = Flask("app")

@app.route('/<int:id>', methods = ['GET'])
def home_get(id):
    '''
    Makes a request for the entry under id
    EXAMPLE: curl -XGET localhost:5000/0
    RETURNS: data under servername.com/id
    '''
    global SIMPLE_STORAGE
    data = SIMPLE_STORAGE.get(id)
    if data:
        result_code = SUCCESSFUL_CODE
    else:
        data = ID_ERROR
        result_code = 404    
    response = Response(response = json.dumps(data), status = result_code)
    return response

@app.route('/<int:id>', methods = ['PUT'])
def home_put(id):
    '''
    Modifies entry in database under id
    EXAMPLE: curl -XPUT localhost:5000/0 -H "Content-Type: application/json" -d '{"sample": "2"}'
    RETURNS: id of changed data
    '''
    global SIMPLE_STORAGE
    SIMPLE_STORAGE[id] = request.json
    response = Response(response = json.dumps({"changed" :id}), status = SUCCESSFUL_CODE)
    return response

@app.route('/', methods = ['POST'])
def home_post():
    '''
    Creates a new entry in database with next available id
    EXAMPLE: curl -XPOST localhost:5000/ -H "Content-Type: application/json" -d '{"sample": "1"}'
    RETURNS: id of created data and created data
    '''
    global SIMPLE_STORAGE
    global SIMPLE_ID
    SIMPLE_STORAGE[SIMPLE_ID] = request.json
    response = Response(response = json.dumps({"new_id" : SIMPLE_ID, "data": request.json}), status = SUCCESSFUL_CODE)
    SIMPLE_ID += 1
    return response

@app.route('/<int:id>', methods = ['DELETE'])
def home_delete(id):
    '''
    Deletes an entry in database under id
    EXAMPLE: curl -XDELETE localhost:5000/0
    RETURNS: deleted data
    '''
    global SIMPLE_STORAGE
    deleted_item = SIMPLE_STORAGE.pop(id)
    response = Response(response = json.dumps(deleted_item), status = SUCCESSFUL_CODE)
    return response

@app.route('/', methods = ['OPTIONS'])
@app.route('/<int:id>', methods = ['OPTIONS'])
def home_options():
    '''
    Returns all available methods for url in headers
    EXAMPLE: curl -XOPTIONS localhost:5000/
    RETURNS: Bodyless response with allowed methods in headers['Allow']
    '''
    response = Response(status = SUCCESSFUL_CODE)
    return response

@app.after_request
def singed_off_by(response):
    response.headers["Singed-off-by"] = "Anastasia Belova"
    return response

if __name__ == '__main__':
    app.run()