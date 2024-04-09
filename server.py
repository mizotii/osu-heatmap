"""backend"""

import requests
from config import client_credentials, database, endpoints, get_headers
from flask import Flask, jsonify, redirect, request, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from models import init_db, db, User
from urllib.parse import urlencode, urljoin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database['DB_URI']
init_db(app)
migrate = Migrate(app, db)
CORS(app, resources={r"/config": {"origins": ["http://localhost:8000", "http://localhost:8080"]}})

@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')

@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

@app.route("/profile/<id>")
def profile():
    return

@app.route("/authorize")
def auth_redirect():
    url = create_auth_url()
    return jsonify(url)

@app.route("/callback")
def callback():
    code = request.args.get('code')
    token_data = get_token_data(code)
    store_token(token_data)
    return redirect("/")

def create_auth_url():
    payload = {
        'client_id': client_credentials['CLIENT_ID'],
        'redirect_uri': endpoints['REDIRECT_URI'],
        'response_type': 'code',
        'scope': 'public identify',
        'state': 'randomval',
    }
    query = urlencode(payload)
    url = urljoin(endpoints['BASE_URL'] + endpoints['AUTHORIZATION'], '?' + query)
    return url

def get_this_user(access_token):
    response = requests.get(
        endpoints['BASE_URL'] + endpoints['THIS_USER'],
        headers=get_headers(False, access_token)
    )
    return response.json()

def get_token_data(code):
    payload = {
        'client_id': client_credentials['CLIENT_ID'],
        'client_secret': client_credentials['CLIENT_SECRET'],
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': endpoints['REDIRECT_URI'],
    }
    response = requests.post(
        endpoints['BASE_URL'] + endpoints['TOKEN'],
        headers=get_headers(True),
        data=payload
    )
    return response.json()

def store_token(token_data):
    access_token = token_data['access_token']
    user = get_this_user(access_token)
    db.session.add(
        User(
            id=user.get('id'),
            name=user.get('username'),
            access=access_token,
            expires=token_data['expires_in'],
            refresh=token_data['refresh_token'],
            type=token_data['token_type']
        )
    )
    db.session.commit()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
