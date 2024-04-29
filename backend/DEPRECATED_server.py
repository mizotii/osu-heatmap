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
app.config['SQLALCHEMY_DATABASE_URI'] = sc.database['DB_URI']
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
    user = sc.get_user_out('id', path, as_dict=True)
    if user:
        user_token = sc.get_token_out('user_id', user['id'], as_dict=True)
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
    user = sc.get_user_out('name', username, as_dict=True)
    if user:
        user_id = user['id']
        user_token = sc.get_token_out('user_id', user_id, as_dict=True)
        sc.get_user_in('update', user_token)
        response['USER_FOUND'] = True
        response['USER_ID'] = user_id
        response['SCORES'] = sc.select_all(Score, 'timestamp', 'user_id', user_id)
        response['HEATMAP_DATA'] = sc.scores_to_heatmap(response['SCORES'])
    return jsonify(response)

# todo: make this a function in config
@app.route("/api/profile/<int:id>")
def fetch_profile(id):
    user = sc.get_user_out('id', id, as_dict=True)
    response = sc.profile_data
    response['USERNAME'] = user['name']
    response['GLOBAL_RANK'] = user['global_rank']
    response['SCORES'] = sc.select_all(Score, 'timestamp', 'user_id', id)
    response['HEATMAP_DATA'] = sc.scores_to_heatmap(response['SCORES'])
    return jsonify(response)

@app.route("/callback")
def callback():
    code = request.args.get('code')
    token_data = sc.get_token_data(code)
    sc.get_user_in('update', token_data)
    return redirect("/")

@app.route("/delete_expired_tokens")
def delete_expired_tokens():
    sc.delete_expired_tokens()
    return redirect("/")

def queue_daily(table, sort_by, operation_type, interval):
    objects = sc.select_all(table, sort_by)
    for object in objects:
        scheduler.add_job(sc.get_user_in(operation_type, object), 'interval', seconds=interval)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
    scheduler.start()
    scheduler.add_job(queue_daily(Token, 'expires_at', 'refresh', sc.get_interval('REFRESH_TOKEN')), 'cron', hour='*/12')
    scheduler.add_job(queue_daily(User, 'last_updated', 'update', sc.get_interval('REFRESH_PROFILE')), 'cron', hour='*/2')
    scheduler.shutdown()