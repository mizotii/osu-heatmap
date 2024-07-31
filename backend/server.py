"""backend"""
import pydash as _
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from backend.config.authentication import authorization as au
from config import server_config as sc
from datetime import date, datetime, timedelta
from flask import Flask, jsonify, redirect, request, send_from_directory, session
from flask_migrate import Migrate
from flask_session import Session
from models import init_db, db, Token, User, UserDailyStatistics
from sqlalchemy import and_, exists

scheduler = BackgroundScheduler()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = sc.database['db_uri']
init_db(app)
migrate = Migrate(app, db)

@app.route('/')
def base():
    return send_from_directory('../client/public', 'index.html')

@app.route('/<path:path>')
def home(path):
    return send_from_directory('../client/public', path)

@app.route('/authorize')
def authorize():
    return jsonify(au.build_url())

@app.route('/login')

@app.route('/callback')
def callback():
    return


if __name__ == '__main__':
    app.run(debug=True)