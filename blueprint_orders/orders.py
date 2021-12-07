from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, jsonify
from db.dbcm import make_query
import json
import time
import datetime

from blueprint_auth.auth import user_level_requires

orders = Blueprint('orders', __name__, template_folder='templates')


def render_dishes(db_config):
    db_query = 'SELECT * FROM menu'
    try:
        d_data = make_query(db_config, db_query, [], description=True)
    except ValueError:
        print('ValueError')

    db_query = 'SELECT m.id as dish_id, m.title as title, b.amount as amount, m.cost * b.amount as total FROM basket b INNER JOIN menu m ON b.dish_id = m.id WHERE b.user_id = %s'
    try:
        b_data = make_query(db_config, db_query, [str(session.get('user_id'))], description=True)
    except ValueError:
        print('ValueError')

    if int(session.get('level')) < 1:
        db_query = 'SELECT * FROM orders WHERE customer_id = %s'
        try:
            o_data = make_query(db_config, db_query, [str(session.get('user_id'))], description=True)
        except ValueError:
            print('ValueError')
    else:
        db_query = 'SELECT * FROM orders'
        try:
            o_data = make_query(db_config, db_query, [], description=True)
        except ValueError:
            print('ValueError')

    return render_template('orders.html', title="Управление блюдами", dish_data=d_data, basket_data=b_data, orders_data=o_data)


@orders.route('/', methods=['GET'])
@user_level_requires(0)
def index():
    with open('configs/db_config.json', 'r') as f_conf:
        db_config = json.load(f_conf)

    if request.method == 'GET':
        return render_dishes(db_config)


@orders.route('/order', methods=['GET', 'POST', 'DELETE'])
@user_level_requires(0)
def order():
    with open('configs/db_config.json', 'r') as f_conf:
        db_config = json.load(f_conf)

    request_json = request.get_json()

    if request.method == 'GET':
        query_res = []
        db_query = 'SELECT od.dish_id, m.title, od.amount, od.amount * m.cost as total FROM order_dishes od INNER JOIN menu m ON od.dish_id = m.id WHERE order_id = %s'
        try:
            query_res = make_query(db_config, db_query, [request.args.get('order_id')], description=True)
        except ValueError:
            print('ValueError')

        return jsonify({'order_dishes': query_res})

    elif request.method == 'POST':
        query_res = []
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')

        db_query = 'INSERT INTO orders VALUES (NULL, %s, (SELECT SUM(m.cost * b.amount) FROM basket b INNER JOIN menu m ON b.dish_id = m.id WHERE b.user_id = %s), %s)'
        try:
            make_query(db_config, db_query, [timestamp, str(session.get('user_id')), str(session.get('user_id'))])
        except ValueError:
            print('ValueError')

        db_query = 'SELECT MAX(id) FROM orders'
        try:
            query_res = make_query(db_config, db_query, [])
        except ValueError:
            print('ValueError')

        db_query = 'INSERT INTO order_dishes (order_id, dish_id, amount) SELECT %s, dish_id, amount FROM basket WHERE user_id = %s'
        try:
            make_query(db_config, db_query, [query_res[0][0], str(session.get('user_id'))])
        except ValueError:
            print('ValueError')

        db_query = 'DELETE FROM basket WHERE user_id = %s'
        try:
            make_query(db_config, db_query, [str(session.get('user_id'))])
        except ValueError:
            print('ValueError')

    elif request.method == 'DELETE':
        if int(session.get('level')) > 0:
            db_query = 'DELETE FROM orders WHERE id = %s'
            try:
                make_query(db_config, db_query, [request_json['order_id']])
            except ValueError:
                print('ValueError')

        else:
            db_query = 'DELETE FROM orders WHERE id = %s AND customer_id = %s'
            try:
                make_query(db_config, db_query, [request_json['order_id'], str(session.get('user_id'))])
            except ValueError:
                print('ValueError')

    return {'status': 'ok'}


@orders.route('/basket', methods=['POST', 'PUT', 'DELETE'])
@user_level_requires(0)
def basket_create():
    with open('configs/db_config.json', 'r') as f_conf:
        db_config = json.load(f_conf)

    request_json = request.get_json()

    if request.method == 'POST':
        db_query = 'SELECT id FROM basket WHERE dish_id = %s AND user_id = %s'
        try:
            query_res = make_query(db_config, db_query, [request_json['dish_id'], str(session.get('user_id'))])
        except ValueError:
            print('ValueError')

        if len(query_res) == 0:
            db_query = 'INSERT INTO basket VALUES (NULL, %s, %s, %s)'
            try:
                make_query(db_config, db_query, [str(session.get('user_id')), request_json['dish_id'], request_json['amount']])
            except ValueError:
                print('ValueError')
        else:
            db_query = 'UPDATE basket b SET amount = %s + b.amount WHERE dish_id = %s AND user_id = %s'
            try:
                make_query(db_config, db_query, [request_json['amount'], request_json['dish_id'], str(session.get('user_id'))])
            except ValueError:
                print('ValueError')

    elif request.method == 'PUT':
        db_query = 'UPDATE basket SET amount = %s WHERE dish_id = %s AND user_id = %s'
        try:
            make_query(db_config, db_query, [request_json['amount'], request_json['dish_id'], str(session.get('user_id'))])
        except ValueError:
            print('ValueError')

    elif request.method == 'DELETE':
        db_query = 'DELETE FROM basket WHERE dish_id = %s AND user_id = %s'
        try:
            make_query(db_config, db_query, [request_json['dish_id'], str(session.get('user_id'))])
        except ValueError:
            print('ValueError')

    return {'status': 'ok'}

