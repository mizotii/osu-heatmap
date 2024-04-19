"""backend"""

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from config import attributes, automatic_intervals, client_credentials, database, endpoints, get_headers, get_user_score_endpoint, profile_data, score_parameters, user_search
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
    update_user(path)
    return send_from_directory('../client/public', 'index.html')

@app.route("/authorize")
def auth_redirect():
    url = create_auth_url()
    return jsonify(url)

@app.route("/api/search/<username>")
def search(username):
    response = user_search
    id = get_id_from_username(username)
    if id != None:
        update_user(id)
        response['USER_FOUND'] = True
        response['USER_ID'] = id
    return jsonify(response)

@app.route("/api/profile/<int:id>")
def fetch_profile(id):
    response = profile_data
    response['USERNAME'], response['GLOBAL_RANK'] = db.session.query(User.name, User.global_rank).where(User.id == id).first()
    response['SCORES'] = db.session.query(Score).where(Score.user_id == id).all()
    return jsonify(response)

@app.route("/callback")
def callback():
    code = request.args.get('code')
    token_data = get_token_data(code)
    store_user(token_data)
    return redirect("/")

# todo: payload -> config
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

def fetch_access_from_id(id):
    print(db.session.query(User.access).where(User.id == id).scalar())
    return db.session.query(User.access).where(User.id == id).scalar()

def get_id_from_username(username):
    return db.session.query(User.id).where(User.name == username).scalar()

# returns the User object as described in osu!API
def get_this_user(access_token):
    response = requests.get(
        endpoints['BASE_URL'] + endpoints['V2'] + endpoints['THIS_USER'],
        headers=get_headers(False, access_token)
    )
    return response.json()

# todo: payload -> config
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

# todo: maybe make the two below functions into one later
def get_username_from_id(id):
    return db.session.query(User.name).where(User.id == id).scalar()

def get_user_data(id):
    return db.session.query(User).where(User.id == id).first()

def get_user_attribute(user, column):
    column = attributes.get(column)
    if '.' in column:
        keys = column.split('.')
        for key in keys:
            user = user.get(key)
        return user
    return user.get(column)

# todo
def refresh_tokens():
    return

def store_user(token_data):
    access_token = token_data['access_token']
    new_user = get_this_user(access_token)
    username = new_user.get('username')
    if user_exists(username):
        old_user = get_user_data(new_user.get('id'))
        for column in User.__table__.columns:
            if getattr(old_user, column.key) is None:
                setattr(old_user, column.key, get_user_attribute(new_user, column.key))
                db.session.add(old_user)
    else:
        db.session.add(
            User(
                id=new_user.get('id'),
                name=username,
                global_rank=new_user.get('statistics', {}).get('global_rank'),
                access=access_token,
                expires=token_data['expires_in'],
                refresh=token_data['refresh_token'],
                type=token_data['token_type'],
            )
        )
    db.session.commit()

def total_hits(score_statistics):
    return score_statistics.get('count_300') + score_statistics.get('count_100') + score_statistics.get('count_50')

# todo: update all user attributes, not just scores
def update_user(user_id):
    response = requests.get(
        endpoints['BASE_URL'] + endpoints['V2'] + get_user_score_endpoint('8816844'),
        headers=get_headers(False, fetch_access_from_id(user_id)),
        data=score_parameters
    )
    scores = response.json()
    print(scores)
    for score in scores:
        score_id = score.get('id')
        if not score_exists(score_id):
            db.session.add(
                Score(
                    id=score_id,
                    user_id=score.get('user_id'),
                    timestamp=datetime.fromisoformat(score.get('ended_at')),
                    notes=(total_hits(score.get('statistics'))),
                    accuracy=score.get('accuracy'),
                )
            )
    db.session.commit()

# todo: these are prob redundant. glad i organize functions alphabetically
def user_exists(username):
    return db.session.query(exists().where(User.name == username)).scalar()

def score_exists(score_id):
    return db.session.query(exists().where(Score.id == score_id)).scalar()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
    scheduler = BackgroundScheduler()
