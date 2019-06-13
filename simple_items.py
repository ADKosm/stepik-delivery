from flask import Flask
from flask import request
from flask_cors import CORS
import json


app = Flask(__name__)
CORS(app)

items = [
    'one', 'two', 'three'
]

# POST /items -> {'item': "four"}


@app.route('/items', methods=['GET', 'POST'])
def items_route():
    if request.method == 'GET':
        return json.dumps(items)
    elif request.method == 'POST':
        raw_data = request.data.decode("utf-8")
        data = json.loads(raw_data)
        items.append(data['item'])
        return ""


@app.route('/items/<num>')
def item_one(num):
    number = int(num)
    if number >= 0 and number < len(items):
        return items[number]
    else:
        return "", 404

app.run('0.0.0.0', 8080)
