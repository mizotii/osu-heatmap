"""backend"""

import time
import os
from config import server_config as sc
from datetime import datetime
from flask import Flask, jsonify, redirect, request, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from models import init_db, db, Score

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = sc.database['DB_URI']
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
    user = sc.get_user_out('id', path, False)
    if user:
        user_token = sc.get_token_out('user_id', user['id'], False)
        sc.get_user_in('update', user_token)
    return send_from_directory('../client/public', 'index.html')

@app.route("/authorize")
def auth_redirect():
    url = sc.create_auth_url()
    return jsonify(url)

# todo: make this a function in config
@app.route("/api/search/<username>")
def search(username):
    response = sc.user_search
    user = sc.get_user_out('name', username, False)
    if user:
        user_id = user['id']
        user_token = sc.get_token_out('user_id', user_id, False)
        sc.get_user_in('update', user_token)
        response['USER_FOUND'] = True
        response['USER_ID'] = user_id
    return jsonify(response)

# todo: make this a function in config
@app.route("/api/profile/<int:id>")
def fetch_profile(id):
    user = sc.get_user_out('id', id, False)
    response = sc.profile_data
    response['USERNAME'] = user['name']
    response['GLOBAL_RANK'] = user['global_rank']
    # todo: create standalone for fetching scores
    response['SCORES'] = db.session.query(Score).where(Score.user_id == id).all()
    return jsonify(response)

@app.route("/callback")
def callback():
    code = request.args.get('code')
    token_data = sc.get_token_data(code)
    sc.get_user_in('update', token_data)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
    sc.scheduler.start()
