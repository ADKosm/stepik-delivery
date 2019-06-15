import json
import os
import random
import sqlite3
import urllib

import requests
from flask import Flask

app = Flask(__name__)


def get_cursor():
    connection = sqlite3.connect("database.db")
    c = connection.cursor()
    return c


USER_ID = 1


def init_db():
    c = get_cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS meals (
        id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
        title text,
        available integer,
        picture text,
        price real,
        category integer
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS promocodes (
        id integer PRIMARY KEY,
        code text,
        discount real
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id integer PRIMARY KEY,
        promocode text
    ) 
    """)

    c.execute("""
    INSERT INTO meals VALUES (1, "Chicken", 1, "", 20.0, 1)
    """)
    c.execute("""
    INSERT INTO meals VALUES (2, "Milk", 1, "", 10.0, 1)
    """)

    c.execute("""
    INSERT INTO promocodes VALUES (1, "stepik", 30.0)
    """)
    c.execute("""
    INSERT INTO promocodes VALUES (2, "delivery", 20.0)
    """)

    c.execute("""
    INSERT INTO users VALUES (1, null)
    """)
    c.connection.commit()
    c.connection.close()


def fill_database():
    """
    See https://www.food2fork.com/
    :return:
    """
    api_key = "f96f947346e0439bf62117e1c291e685"
    key_words = "cake"
    c = get_cursor()
    for page in range(1, 2):
        params = urllib.parse.urlencode({'key': api_key, 'q': key_words, 'page': page})
        url_string = "https://www.food2fork.com/api/search?" + params
        r = requests.get(url_string)
        data = r.json()
        for recipe in data['recipes']:
            c.execute("""
            INSERT INTO meals (title, available, picture, price, category) VALUES (?, ?, ?, ?, ?)
            """, [
                recipe['title'],
                1,
                recipe['image_url'],
                recipe['social_rank'] + random.randint(0, 100),
                1
            ])
            c.connection.commit()
    c.connection.close()


@app.route("/promo/<code>")
def promo(code):
    c = get_cursor()
    c.execute("""
    SELECT * FROM promocodes WHERE code = ?
    """, (code, ))
    result = c.fetchone()
    if result is None:
        return json.dumps({'valid': False})

    promo_id, promo_code, promo_discount = result

    c.execute("""
    UPDATE users
    SET promocode=?
    WHERE id = ?
    """, (code, USER_ID))
    c.connection.commit()
    c.connection.close()

    return json.dumps({'valid': True, 'discount': promo_discount})


@app.route("/meals")
def meals():
    c = get_cursor()

    c.execute("""
    SELECT discount 
    FROM promocodes
    WHERE code = (
        SELECT promocode
        FROM users
        WHERE id = ?
    )
    """, (USER_ID,))
    result = c.fetchone()

    discount = 0
    if result is not None:
        discount = result[0]

    meals = []
    for meal_info in c.execute("SELECT * FROM meals"):
        meal_id, title, available, picture, price, category = meal_info
        meals.append({
            'id': meal_id,
            'title': title,
            'available': bool(available),
            'picture': picture,
            'price': price * (1.0-discount/100),
            'category': category
        })
    return json.dumps(meals)


if not os.path.exists("database.db"):
    init_db()
    fill_database()


app.run('0.0.0.0', 8000)