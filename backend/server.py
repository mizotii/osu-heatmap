"""backend"""

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from config import attributes, authentication_payload, automatic_intervals, client_credentials, database, endpoints, get_headers, get_refresh_payload, get_token_payload, get_user_score_endpoint, profile_data, score_parameters, user_search
from datetime import datetime
from flask import Flask, jsonify, redirect, request, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from models import init_db, db, Score, User
from sqlalchemy import exists
from urllib.parse import urlencode, urljoin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database['DB_URI']
init_db(app)
migrate = Migrate(app, db)
CORS(app, resources={r"/config": {"origins": ["http://localhost:8000", "http://localhost:8080"]}})

@app.route("/")
def base():
    return send_from_directory('../client/public', 'index.html')

@app.route("/<path:path>")
def home(path):
    return send_from_directory('../client/public', path)

@app.route("/profile/<path:path>")
def profile(path):
    user = get_user_out('name', path, False)
    if user:
        get_user_in('update', user)
    return send_from_directory('../client/public', 'index.html')

@app.route("/authorize")
def auth_redirect():
    url = create_auth_url()
    return jsonify(url)

@app.route("/api/search/<username>")
def search(username):
    response = user_search
    user = get_user_out('name', username, False)
    if user:
        get_user_in('update', user)
        response['USER_FOUND'] = True
        response['USER_ID'] = getattr(user, 'id')
    return jsonify(response)

@app.route("/api/profile/<int:id>")
def fetch_profile(id):
    user = get_user_out('id', id, False)
    response = profile_data
    response['USERNAME'] = user.get('name')
    response['GLOBAL_RANK'] = user.get('global_rank')
    response['SCORES'] = db.session.query(Score).where(Score.user_id == id).all()
    return jsonify(response)

@app.route("/callback")
def callback():
    code = request.args.get('code')
    token_data = get_token_data(code)
    get_user_in('update', token_data)
    return redirect("/")

def create_auth_url():
    query = urlencode(authentication_payload)
    url = urljoin(endpoints['BASE_URL'] + endpoints['AUTHORIZATION'], '?' + query)
    return url

def get_token_data(code):
    response = requests.post(
        endpoints['BASE_URL'] + endpoints['TOKEN'],
        headers=get_headers(True),
        data=get_token_payload(code)
    )
    return response.json()

# functions as a user presence checker if last arg is True
def get_user_out(attribute_type, value, check_presence_only=None):
    valid_attributes = User.__table__.columns.keys()
    if attribute_type not in valid_attributes:
        raise ValueError(write_value_error(attribute_type, valid_attributes))
    if check_presence_only:
        return db.session.query(exists().where(getattr(User, attribute_type) == value)).scalar()
    else:
        return db.session.query(User).where(getattr(User, attribute_type) == value).first()

# also accepts a User object as valid token data
def get_user_in(operation_type, token_data):
    valid_operations = ['refresh', 'update']
    if operation_type not in valid_operations:
        raise ValueError(write_value_error(operation_type, valid_operations))
    
    access = getattr(token_data, 'access_token')
    refresh = getattr(token_data, 'refresh_token')

    # creates a new user if they aren't found, updates an old user if they are
    if operation_type == 'update':
        response = requests.get(
            endpoints['BASE_URL'] + endpoints['V2'] + endpoints['THIS_USER'],
            headers=get_headers(access)
        )
        new_user_data = response.json()
        new_user_id = new_user_data.get('id')

        # if user exists
        if get_user_out('id', new_user_id, True):
            old_user_data = get_user_out('id', new_user_id, False)
            for key in User.__table__.columns.keys():
                if key is not id:
                    setattr(old_user_data, key, getattr(new_user_data, key))

        # if user is new
        else:
            db.session.add(
                User(
                    id=new_user_id,
                    name=new_user_data.get('username'),
                    global_rank=new_user_data.get('statistics', {}).get('global_rank'),
                    access_token=access,
                    expires_in=getattr(token_data, 'expires_in'),
                    refresh_token=refresh,
                    token_type=getattr(token_data, 'token_type'),
                )
            )

    # refreshes token
    else:
        old_user_data = get_user_out('refresh', refresh, False)
        new_token = refresh_token(refresh)
        for key in new_token.keys():
            setattr(old_user_data, key, getattr(new_token, key))

    # applies to either operation
    db.session.commit()

def refresh_token(refresh_token):
    response = requests.post(
        endpoints['BASE_URL'] + endpoints['TOKEN'],
        headers=get_headers(True),
        data=get_refresh_payload(refresh_token)
    )
    return response.json()

def write_value_error(invalid, valid):
    return f'invalid type \'{invalid}. valid types: {', '.join(valid)}.'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
    scheduler = BackgroundScheduler()
