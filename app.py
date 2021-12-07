from flask import Flask, render_template, request, session

from blueprint_query.query import query
from blueprint_auth.auth import auth
from blueprint_profile.profile import profile
from blueprint_dishes.dishes import dishes
from blueprint_orders.orders import orders

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = '7l{WAB}B$ZRDzQpwvQ$INt7MTUN|0$4M'
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(query, url_prefix='/query')
app.register_blueprint(profile, url_prefix='/profile')
app.register_blueprint(dishes, url_prefix='/dishes')
app.register_blueprint(orders, url_prefix='/orders')


@app.route('/')
def index():
    return render_template('index.html', title='Главная')


if __name__ == '__main__':
    app.run(host='localhost', port=1338)
