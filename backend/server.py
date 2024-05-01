"""backend"""

import time
import os
from apscheduler.schedulers.background import BackgroundScheduler
from config import server_config as sc
from datetime import datetime
from flask import Flask, jsonify, redirect, request, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from models import init_db, db, Score, Token, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = sc.database['db_uri']
init_db(app)
migrate = Migrate(app, db)
CORS(app, resources={r"/config": {"origins": ["http://localhost:8000", "http://localhost:8080"]}})

scheduler = BackgroundScheduler()

@app.route("/")
def base():
    return send_from_directory('../client/public', 'index.html')

@app.route("/<path:path>")
def home(path):
    return send_from_directory('../client/public', path)

@app.route("/profile/<path:path>")
def profile(path):
    return

@app.route("/authorize")
def auth_redirect():
    return jsonify(sc.create_authorization_url())

@app.route("/api/search/<username>")
def search(username):
    return

# todo: make this a function in config
@app.route("/api/profile/<int:id>")
def fetch_profile(id):
    return

@app.route("/callback")
def callback():
    code = request.args.get('code')
    token = sc.fetch_token(code)
    sc.after_authorization(token, code)
    return redirect("/")

@app.route("/delete_expired_tokens")
def delete_expired_tokens():
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)