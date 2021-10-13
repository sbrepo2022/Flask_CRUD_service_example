from flask import Flask, Blueprint, render_template, request
from db.dbcm import make_query
import json

from blueprint_auth.auth import user_level_requires

query = Blueprint('query', __name__, template_folder='templates')


@query.route('/')
@user_level_requires(0)
def index():
    with open('blueprint_query/configs/query_config.json', 'r') as f_conf:
        query_config = json.load(f_conf)
    query_links = [{'link': key, 'description': query_config[key]["description"]} for key in query_config.keys()]
    return render_template('index_query.html', title='Запросы', query_links=query_links)


@query.route('/<path>', methods=['GET', 'POST'])
@user_level_requires(0)
def form(path):
    if request.method == 'GET':
        with open('blueprint_query/configs/query_config.json', 'r') as f_conf:
            query_config = json.load(f_conf)
        return render_template('query_form.html', title='Форма запроса', form_data=query_config[path])
    elif request.method == 'POST':
        query_data = db_query_request(path, request.form)
        return render_template('query_result.html', title='Результат запроса', query_sql=query_data['query_sql'], table_data=query_data['table_data'])


def db_query_request(path, form_data):
    with open('configs/db_config.json', 'r') as f_conf:
        db_config = json.load(f_conf)

    with open('blueprint_query/configs/query_config.json', 'r') as f_conf:
        query_config = json.load(f_conf)

    # setting query and it's parameters
    if path in query_config:
        db_query = query_config[path]['query']
        query_params = [form_data[param] for param in query_config[path]['params']]

        try:
            return {
                'query_sql': db_query % tuple(query_params),
                'table_data': make_query(db_config, db_query, query_params, description=True)
            }
        except ValueError:
            print('ValueError')
    return None

