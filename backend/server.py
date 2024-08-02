"""backend"""
import pydash as _
import requests
import secrets
from apscheduler.schedulers.background import BackgroundScheduler
from config.authentication import authorization as au
from config.authentication import callback as cb
from config.authentication import login as lg
from config.osu_api import fetch as ft
from db import update as up
from db import read as rd
from config import server_config as sc
from datetime import date, datetime, timedelta
from flask import Flask, jsonify, redirect, request, send_from_directory, session
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_migrate import Migrate
from flask_session import Session
from db.models import init_db, db, Token, User, UserDailyStatistics
from sqlalchemy import and_, exists

scheduler = BackgroundScheduler()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = sc.database['db_uri']
app.secret_key = sc.credentials['sessions_key']
init_db(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def base():
    return send_from_directory('../client/public', 'index.html')

@app.route('/<path:path>')
def home(path):
    return send_from_directory('../client/public', path)

@login_manager.user_loader
def load_user(id):
    return User.get(id)

@app.route('/authorize')
def authorize():
    session['state'] = secrets.token_urlsafe(16)
    return jsonify(au.build_url(session['state']))

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/', authenticated=False)

@app.route('/callback')
def callback():
    # grab code
    code = request.args.get('code')

    # get access token
    token = cb.request_token(code)

    # search for user, if they don't exist, store them
    id = ft.fetch_user(token['access'])
    user = rd.read_user(id)
    
    if not user:
        up.store_token(token, id)

    login_user(user)

    return redirect('/', authenticated=True)

@app.route('api/get_session')
def get_session():
    return current_user.is_authenticated

if __name__ == '__main__':
    app.run(debug=True)