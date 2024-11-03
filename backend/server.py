"""backend"""
import logging
import pydash as _
import requests
import redis
import secrets
import sys
from api import create as cr
from apscheduler.schedulers.background import BackgroundScheduler
from config.authentication import authorization as au
from config.authentication import callback as cb
from config.osu_api import fetch as ft
from db import update as up
from db import read as rd
from config import server_config as sc
from datetime import datetime
from flask import Flask, jsonify, redirect, request, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_migrate import Migrate
from flask_session import Session
from db.models import init_db, db

scheduler = BackgroundScheduler()
session = Session()

app = Flask(__name__,
    static_folder='../client/public/',
)
app.config['SQLALCHEMY_DATABASE_URI'] = sc.database['db_uri']
# app.secret_key = sc.credentials['sessions_key']
app.config['SECRET_KEY'] = sc.credentials['sessions_key']
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)
init_db(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
CORS(app, supports_credentials=True, origins=sc.endpoints['frontend'])
app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True
)
session.init_app(app)

@app.route('/')
def base():
    return send_from_directory('../client/public', 'index.html')

@app.route("/<path:any>/static/<path:path>")
def icons(any, path):
    return send_from_directory('../client/public/static', path)

@login_manager.user_loader
def load_user(id):
    return rd.read_user(id)

@app.route('/authorize')
def authorize():
    state = secrets.token_urlsafe(16)
    return jsonify(au.build_url(state))

@app.route('/api/logout')
@login_required
def logout():
    logout_user()
    return redirect(sc.endpoints['frontend'])

@app.route('/callback')
def callback():
    # grab code
    code = request.args.get('code')

    # get access token
    token = cb.request_token(code)
    access = token['access_token']

    # search for user, if they don't exist, store them
    fetched_user = ft.fetch_self(access)
    id = fetched_user['id']
    user = rd.read_user(id)
    
    if not user:
        up.store_user(token, fetched_user)
    else:
        up.update_user_token(token, user)

    user = rd.read_user(id)

    up.update_user_statistics(app, user)

    for ruleset in rulesets:
        up.store_scores(app, id, ruleset)

    # log them in
    login_user(user, remember=True)

    return redirect(f"{sc.endpoints['frontend']}/profile/{id}")

@app.route('/api/search')
def search():
    all_users_query = rd.all_users(app)
    users = []
    for user in all_users_query:
        users.append(user.as_dict())
    return jsonify(users)

@app.route("/api/profile/<int:id>/<string:ruleset>")
@app.route("/api/profile/<int:id>")
def fetch_profile(id, ruleset=None):
    # want profile to route to catch, same as osu!web
    if ruleset == 'catch':
        ruleset = 'fruits'
    if ruleset == 'overall':
        return jsonify(cr.create_profile(id, ruleset, True))
    if not ruleset:
        ruleset = rd.read_user(id).__dict__['playmode']
    
    user = rd.read_user(id)

    up.update_user_statistics(app, user)

    return jsonify(cr.create_profile(id, ruleset, False))

@app.route("/api/scores/<int:id>/<string:ruleset>/<int:timestamp>")
def fetch_scores(id, ruleset, timestamp):
    return jsonify(cr.create_score_list(id, ruleset, timestamp))

@app.route('/api/get_session')
def get_session():
    data = { 
        'login': current_user.is_authenticated,
        'id': current_user.get_id(),
    }
    print(data, flush=True)
    return jsonify(data)

@app.route('/api/get_user_data')
@login_required 
def get_user_data():
    user = (rd.read_user(current_user.id)).__dict__
    return jsonify({ 'id': user['id'], 'username': user['username'], 'avatar_url': user['avatar_url'] })

@app.route('/api/get_user_count')
def get_user_count():
    count = rd.read_user_count()
    return jsonify({ 'count': count })

rulesets = [
    'osu', 'taiko', 'fruits', 'mania',
]

def auto_update():
    users = rd.all_users(app)
    for user in users:
        up.update_user_statistics(app, user)

def auto_refresh_client_key():
    with app.app_context():
        up.refresh_client_credentials()

with app.app_context():
    up.refresh_client_credentials()

logging.basicConfig(level=logging.INFO)
scheduler.add_job(auto_update, 'interval', hours=2)
scheduler.add_job(auto_refresh_client_key, 'interval', hours=6)
scheduler.start()
scheduler.print_jobs()

if __name__ == '__main__':
    app.run(debug=True)