from flask import Flask
from flask import request
from flask_cors import CORS
import json
import random


app = Flask(__name__)
CORS(app)


items = [
    'one', 'two', 'three'
]


@app.route("/items", methods=["GET", "POST", "BIB"])
def pp():
    if request.method == 'GET':
        return json.dumps(items)
    elif request.method == 'POST':
        data = json.loads(request.data.decode('utf-8'))
        items.append(data['item'])
        return ""


@app.route("/items/<num>")
def nn(num):
    return items[int(num)-1]


app.run('0.0.0.0', 8000)
