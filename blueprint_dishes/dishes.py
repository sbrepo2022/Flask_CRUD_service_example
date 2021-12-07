from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
from db.dbcm import make_query
import json

from blueprint_auth.auth import user_level_requires

dishes = Blueprint('dishes', __name__, template_folder='templates')


def render_dishes(db_config):
    db_query = 'SELECT * FROM menu'

    try:
        data = make_query(db_config, db_query, [], description=True)
    except ValueError:
        print('ValueError')

    return render_template('dishes.html', title="Управление блюдами", table_data=data)


@dishes.route('/', methods=['GET', 'POST'])
@user_level_requires(1)
def index():
    with open('configs/db_config.json', 'r') as f_conf:
        db_config = json.load(f_conf)

    if request.method == 'GET':
        return render_dishes(db_config)

    elif request.method == 'POST':
        request_json = request.get_json()
        db_query = 'INSERT INTO menu VALUES (NULL, %s, %s)'

        try:
            make_query(db_config, db_query, [request_json['title'], request_json['cost']])
        except ValueError:
            print('ValueError')

        return {'status': 'ok'}


@dishes.route('/<dish_id>', methods=['PUT', 'DELETE'])
@user_level_requires(1)
def index_actions(dish_id):
    with open('configs/db_config.json', 'r') as f_conf:
        db_config = json.load(f_conf)

    if request.method == 'PUT':
        request_json = request.get_json()
        db_query = 'UPDATE menu SET title = %s, cost = %s WHERE id = %s'

        try:
            make_query(db_config, db_query, [request_json['title'], request_json['cost'], dish_id])
        except ValueError:
            print('ValueError')

        return {'status': 'ok'}

    elif request.method == 'DELETE':
        db_query = 'DELETE FROM menu WHERE id = %s'

        try:
            make_query(db_config, db_query, [dish_id])
        except ValueError:
            print('ValueError')

        return {'status': 'ok'}