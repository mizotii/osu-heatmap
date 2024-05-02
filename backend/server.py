"""backend"""

import time
import os
import pydash as _
from apscheduler.schedulers.background import BackgroundScheduler
from config import server_config as sc
from datetime import datetime, timedelta
from flask import Flask, jsonify, redirect, request, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from models import init_db, db, Class, Score, Token, User, UserDailyStatistics

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

def queue_dailies(date):
    previous_user_objects = sc.select_all(User, sort_by=User.last_updated, as_dict=True)
    interval = (sc.intervals['dailies']['interval'] * sc.intervals['hours_to_seconds']) / len(previous_user_objects)
    total_interval = 0
    for previous_user in previous_user_objects:
        id = previous_user['id']
        token = sc.get_object(Token, 'id', id, as_dict=True)
        for ruleset in sc.rulesets:
            if not sc.get_object(UserDailyStatistics, 'id', id, check_exists_only=True):
                previous_user_ruleset = sc.get_object(sc.tables[ruleset], 'id', id, as_dict=True)
                sc.direct_update_user(id, token, ruleset)
                new_user_ruleset = sc.get_object(sc.tables[ruleset], 'id', id, as_dict=True)
                play_time = _.get(new_user_ruleset, sc.user_attributes['play_time']) - _.get(previous_user_ruleset, sc.user_attributes['play_time'])
                play_count = _.get(new_user_ruleset, sc.user_attributes['play_count']) - _.get(previous_user_ruleset, sc.user_attributes['play_count'])
                note_count = _.get(new_user_ruleset, sc.user_attributes['total_hits']) - _.get(previous_user_ruleset, sc.user_attributes['total_hits'])
                ranked_score = _.get(new_user_ruleset, sc.user_attributes['ranked_score']) - _.get(previous_user_ruleset, sc.user_attributes['ranked_score'])
                total_score = _.get(new_user_ruleset, sc.user_attributes['total_score']) - _.get(previous_user_ruleset, sc.user_attributes['total_score'])
                scheduler.add_job(sc.score_daily_statistics, 'date', run_date=(datetime.now() + timedelta(seconds=total_interval)), args=[id, ruleset, date, play_time, play_count, note_count, ranked_score, total_score])
                total_interval += interval

def queue_refresh():
    tokens = sc.select_all(Token, sort_by=Token.expires_at)
    interval = ((sc.intervals['hours'] / int(sc.intervals['refresh']['interval']).strip('*/')) * sc.intervals['hours_to_seconds']) / len(tokens)
    total_interval = 0
    for token in tokens:
        scheduler.add_job(sc.refresh_token, 'date', run_date=(datetime.now() + timedelta(seconds=total_interval)), args=[token])
        total_interval += interval

def queue_users():
    tokens = sc.select_all(Token, join_by_table=User, join_by_column_other=User.id, join_by_column_this=Token.user_id, sort_by=User.last_updated, as_dict=True)
    interval = ((sc.intervals['hours'] / int(sc.intervals['users']['interval']).strip('*/')) * sc.intervals['hours_to_seconds']) / (len(tokens) * len(sc.rulesets))
    total_interval = 0
    for token in tokens:
        id = token['user_id']
        scheduler.add_job(sc.update_user_scores, 'date', run_date=(datetime.now() + timedelta(seconds=total_interval)), args=[id])
        for ruleset in sc.rulesets:
            scheduler.add_job(sc.direct_update_user, 'date', run_date=(datetime.now() + timedelta(seconds=total_interval)), args=[id, token, ruleset])
            total_interval += interval

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
    scheduler.add_job(queue_dailies, 'cron', hour=sc.intervals['dailies']['hour'], args=[(datetime.now().date - timedelta(days=1))])
    scheduler.add_job(queue_refresh, 'cron', hour=sc.intervals['refresh']['interval'])
    scheduler.add_job(queue_users, 'cron', hour=sc.intervals['users']['interval'])