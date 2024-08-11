"""backend"""
import pydash as _
import secrets
from api import create as cr
from apscheduler.schedulers.background import BackgroundScheduler
from api import create as cr
from config.authentication import authorization as au
from config.authentication import callback as cb
from config.authentication import refresh as rf
from config.osu_api import fetch as ft
from db import update as up
from db import read as rd
from config import server_config as sc
from datetime import datetime
from flask import Flask, jsonify, redirect, request, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_migrate import Migrate
from db.models import init_db, db

scheduler = BackgroundScheduler()

app = Flask(__name__,
    static_folder='../client/public/',
)
app.config['SQLALCHEMY_DATABASE_URI'] = sc.database['db_uri']
app.secret_key = sc.credentials['sessions_key']
init_db(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

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

@app.route('/logout')
def logout():
    logout_user()
    return send_from_directory('../client/public', 'index.html')

@app.route('/callback')
def callback():
    # grab code
    code = request.args.get('code')

    # get access token
    token = cb.request_token(code)
    access = token['access_token']

    # search for user, if they don't exist, store them
    fetched_user = ft.fetch_user(access)
    id = fetched_user['id']
    user = rd.read_user(id)
    
    if not user:
        up.store_user(token, fetched_user)
        user = rd.read_user(id)

    # todo: initialize the rest of their data
    up.update_user_statistics(app, user)

    for ruleset in rulesets:
        up.store_scores(app, access, id, ruleset)

    # log them in
    login_user(user)

    # return redirect(f'{sc.endpoints['frontend']}/profile/{id}')
    return send_from_directory('../client/public', 'index.html')

@app.route('/api/search')
def search():
    all_users_query = rd.all_users(app)
    users = []
    for user in all_users_query:
        users.append(user.as_dict())
    return jsonify(users)

@app.route("/profile/<int:id>")
def profile_default(id):
    user = rd.read_user(id)
    access = user.__dict__['access_token']

    up.update_user_statistics(app, user)

    for ruleset in rulesets:
        up.store_scores(app, access, id, ruleset)
        
    return send_from_directory('../client/public', 'index.html')

@app.route("/profile/<int:id>/<string:ruleset>")
def profile_ruleset(id, ruleset):
    user = rd.read_user(id)
    access = user.__dict__['access_token']
    if ruleset == 'catch':
        ruleset = 'fruits'

    up.update_user_statistics(app, user)

    up.store_scores(app, access, id, ruleset)
    return send_from_directory('../client/public', 'index.html')

@app.route("/api/profile/<int:id>/<string:ruleset>")
@app.route("/api/profile/<int:id>")
def fetch_profile(id, ruleset=None):
    # want profile to route to catch, same as osu!web
    if ruleset == 'catch':
        ruleset = 'fruits'
    if not ruleset:
        ruleset = rd.read_user(id).__dict__['playmode']
    return jsonify(cr.create_profile(id, ruleset))

@app.route("/api/scores/<int:id>/<string:ruleset>/<int:timestamp>")
def fetch_scores(id, ruleset, timestamp):
    return jsonify(cr.create_score_list(id, ruleset, timestamp))

@app.route('/api/get_session')
def get_session():
    return jsonify({ 'login': current_user.is_authenticated })

@app.route('/api/get_user_data')
@login_required 
def get_user_data():
    user = (rd.read_user(current_user.id)).__dict__
    return jsonify({ 'username': user['username'], 'avatar_url': user['avatar_url'] })

def refresh_tokens():
    users = rd.all_users(app)
    for user in users:
        if user.__dict__['expires_at'] < datetime.now():
            rf.refresh_token(app, user)

rulesets = [
    'osu', 'taiko', 'fruits', 'mania',
]

def midnight_update():
    users = rd.all_users(app)
    for user in users:
        up.update_user_statistics(app, user)

if __name__ == '__main__':
    scheduler.add_job(midnight_update, 'cron', hour='*')
    scheduler.add_job(refresh_tokens, 'cron', hour='*/2')
    scheduler.start()
    scheduler.print_jobs()
    app.run(debug=True)