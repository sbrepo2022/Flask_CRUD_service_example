from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from db.dbcm import make_query
import json

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/', methods=['GET', 'POST'])
def index():
    if session.get('user_id') is None:
        if request.method == 'GET':
            return render_template('index_auth.html',
                                   title='Вход',
                                   exclude_header=True)
        elif request.method == 'POST':
            user_data = check_register(request.form)
            if user_data is None:
                return render_template('index_auth.html',
                                       title='Вход',
                                       errors=['Неверный логин или пароль'],
                                       exclude_header=True)
            else:
                session['user_id'] = user_data['user_id']
                session['level'] = user_data['level']
                return redirect('/')
    else:
        return redirect('/')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id') is None:
        if request.method == 'GET':
            return render_template('register.html',
                                   title='Регистрация',
                                   exclude_header=True)
        elif request.method == 'POST':
            result = create_user(request.form)
            if not result:
                return render_template('register.html',
                                       title='Регистрация',
                                       errors=['Пользователь с таким логином уже существует'],
                                       exclude_header=True)
            else:
                return redirect(url_for('auth.index'))
    else:
        return redirect('/')


@auth.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@auth.route('/403')
def forbidden():
    return render_template('403.html', title='403 Forbidden')


def check_register(form_data):
    with open('configs/db_config.json', 'r') as f_conf:
        db_config = json.load(f_conf)

    try:
        result = make_query(db_config, 'SELECT id, login, password, level FROM users WHERE login = %s', [form_data['login']])
        if len(result) > 0:
            row = result[0]
            if check_password_hash(row[2], form_data['password']):
                return {'user_id': int(row[0]), 'level': int(row[3])}
        else:
            return None
    except ValueError:
        print('ValueError')
    return None


def create_user(form_data):
    with open('configs/db_config.json', 'r') as f_conf:
        db_config = json.load(f_conf)

    if form_data['password'] != form_data['password2']:
        return False

    try:
        result = make_query(db_config, 'SELECT id FROM users WHERE login = %s', [form_data['login']])
        if len(result) > 0:
            return False

        make_query(db_config, 'INSERT INTO users(login, password) VALUES(%s, %s)', [form_data['login'], generate_password_hash(form_data['password'])])
        return True
    except ValueError:
        print('ValueError')
    return False


def user_level_requires(level: int):
    def user_login_requires(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if session.get('user_id') is None:
                return redirect(url_for('auth.index'))
            if session.get('level') < level:
                return redirect(url_for('auth.forbidden'))
            return f(*args, **kwargs)
        return wrapper
    return user_login_requires


