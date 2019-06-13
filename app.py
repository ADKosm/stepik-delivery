from flask import Flask
from flask import request
from flask_cors import CORS
import json
import random
import uuid


app = Flask(__name__)
CORS(app)


USER_ID = "1"


meals = [{
 "title": "Chinken",
 "id": 1,
 "available": True,
 "picture": "",
 "price": 20.0,
 "category": 1
}, {
 "title": "Milk",
 "id": 2,
 "available": True,
 "picture": "",
 "price": 10.0,
 "category": 1
}]


def promotion():
    promotion_number = random.randint(0, 2)
    promotion_file = open("promotions.json", "r", encoding='CP1251')
    promotions = json.loads(promotion_file.read())
    return json.dumps(promotions[promotion_number], ensure_ascii=False)


def read_file(filename):
    opened_file = open(filename, 'r')
    config_content = opened_file.read()
    data = json.loads(config_content)
    opened_file.close()
    return data


def write_file(filename, data):
    opened_file = open(filename, 'w')
    opened_file.write(json.dumps(data))
    opened_file.close()


@app.route("/alive")
def alive():
    data = read_file('config.json')

    return json.dumps({"alive": data['alive']})


@app.route("/workhours")
def work():
    data = read_file('config.json')

    return json.dumps(data['workhours'])


@app.route("/promotion")
def promotion():
    promotion_number = random.randint(0, 2)
    promotions = read_file('promotions.json')

    print(json.dumps(promotions[promotion_number], ensure_ascii=False))
    return json.dumps(promotions[promotion_number], ensure_ascii=False)


@app.route("/promo/<code>")
def promo(code):
    promocodes = read_file('promo.json')

    for promocode in promocodes:
        if promocode["code"] == code:
            users_data = read_file("users.json")

            users_data[USER_ID]["promocode"] = code

            write_file('users.json', users_data)

            return json.dumps({"valid": True, "discount": promocode['discount']})
    return json.dumps({"valid": False})


@app.route("/ppoosstt", methods=["GET", "POST", "BIB"])
def pp():
    return request.method


@app.route("/meals")
def meals_route():
    users_data = read_file('users.json')

    discount = 0

    promocode = users_data[USER_ID]["promocode"]

    meals_copy = json.loads(json.dumps(meals))

    if promocode != None:
        promocodes = read_file('promo.json')

        for p in promocodes:
            if p['code'] == promocode:
                discount = p['discount']

        for meal in meals_copy:
            meal['price'] = (1.0-discount/100) * meal['price']

    return json.dumps(meals)


"""
  "id1": {
    "id": "id1",
    "meals": [1],
    "summ": 12,
    "status": "canceled",
    "user_id": "1"
  }
"""


@app.route("/orders", methods=["GET", "POST"])
def orders():
    """
    POST /orders -> { meals: [...] }
    :return:
    """
    if request.method == 'GET':
        orders_data = read_file("orders.json")
        user_orders = []
        for order_id in orders_data:
            if orders_data[order_id]['user_id'] == USER_ID:
                user_orders.append(orders_data[order_id])
        return json.dumps(user_orders)
    elif request.method == 'POST':
        raw_data = request.data.decode("utf-8")
        data = json.loads(raw_data)


        discount = 0
        users_data = read_file('users.json')
        promocode = users_data[USER_ID]["promocode"]
        if promocode != None:
            promocodes = read_file('promo.json')
            for p in promocodes:
                if p['code'] == promocode:
                    discount = p['discount']


        summ = 0
        meals_copy = json.loads(json.dumps(meals))
        for meal in meals_copy:
            meal_id = meal['id']
            for user_meal_id in data['meals']:
                if user_meal_id == meal_id:
                    summ = summ + meal['price'] * (1.0-discount/100)
                    break

        new_order_id = str(uuid.uuid4())
        new_order = {
            "id": new_order_id,
            "meals": data['meals'],
            'summ': summ,
            "status": "accepted",
            "user_id": USER_ID
        }

        order_data = read_file("orders.json")
        order_data[new_order_id] = new_order
        write_file('orders.json', order_data)

        return json.dumps({'order_id': new_order_id, "status": new_order['status']})


@app.route("/activeorder")
def actoveorder():
    orders_data = read_file("orders.json")
    user_orders = []
    for order_id in orders_data:
        order = orders_data[order_id]
        if order['user_id'] == USER_ID and order['status'] == 'accepted':
            return json.dumps(order)
    return "", 404


@app.route("/orders/<order_id>", methods=["DELETE"])
def one_order(order_id):
    orders_data = read_file("orders.json")
    for saved_order_id in orders_data:
        order = orders_data[saved_order_id]
        if saved_order_id == order_id and order['user_id'] == USER_ID:
            orders_data[saved_order_id]['status'] = 'cancelled'
            write_file('orders.json', orders_data)
            return json.dumps({'order_id': order_id, "status": "cancelled"})
    return "", 404



app.run('0.0.0.0', 8090)