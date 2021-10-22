from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from db.dbcm import make_query
import json

from blueprint_auth.auth import user_level_requires

profile = Blueprint('profile', __name__, template_folder='templates')

sidebar_config = [
    {
        'name': 'profile',
        'title': 'Профиль',
        'img_src': '/static/resources/icons/profile.svg',
        'link': '/profile'
    },
    {
        'name': 'admin',
        'title': 'Управление',
        'img_src': '/static/resources/icons/admin.svg',
        'link': '/profile/admin'
    }
]

sp_errors = ['Пароли не совпадают']

sp_success = ['Пароль изменен']


@profile.route('/')
@user_level_requires(0)
def index():
    with open('configs/db_config.json', 'r') as f_conf:
        db_config = json.load(f_conf)
    db_query = 'SELECT id, login, password, level FROM users WHERE id = %s'

    try:
        data = make_query(db_config, db_query, session.get('user_id'))[0]
    except ValueError:
        print('ValueError')

    errors = {}
    if request.args.get('sp_error') is not None:
        errors['sp_error'] = sp_errors[int(request.args.get('sp_error'))]

    success = {}
    if request.args.get('sp_success') is not None:
        success['sp_success'] = sp_success[int(request.args.get('sp_success'))]

    return render_template('index_profile.html',
                           title='Профиль',
                           sidebar=sidebar_config,
                           cur_page='profile',
                           data={
                               'login': data[1],
                               'level': data[3]
                           },
                           errors=errors,
                           success=success)


@profile.route('/admin')
@user_level_requires(0)
def admin():
    return render_template('admin.html',
                           title='Управление',
                           sidebar=sidebar_config,
                           cur_page='admin')


@profile.route('/set_password', methods=['POST'])
@user_level_requires(0)
def set_password():
    if request.form['password'] != request.form['password2']:
        return redirect(url_for('profile.index') + f'/?sp_error=0')

    with open('configs/db_config.json', 'r') as f_conf:
        db_config = json.load(f_conf)
    db_query = 'UPDATE users SET password = %s WHERE id = %s'

    try:
        make_query(db_config, db_query, [generate_password_hash(request.form['password']), session.get('user_id')])
    except ValueError:
        print('ValueError')

    return redirect(url_for('profile.index') + f'?sp_success=0')

