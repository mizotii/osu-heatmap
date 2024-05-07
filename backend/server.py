"""backend"""

import time
import os
import pydash as _
from apscheduler.schedulers.background import BackgroundScheduler
from config import server_config as sc
from datetime import date, datetime, timedelta
from flask import Flask, jsonify, redirect, request, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from models import init_db, db, Class, Score, Token, User, UserDailyStatistics
from sqlalchemy import and_, exists

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
    """ruleset = getattr(sc.get_object(User, 'id', path), 'playmode')
    token = sc.get_object(Token, 'user_id', path, as_dict=True)
    sc.direct_update_user(path, token, ruleset)
    sc.update_user_scores(path)"""
    return send_from_directory('../client/public', 'index.html')

@app.route("/profile/<int:id>/<path:path>")
def profile_ruleset(id, path):
    """ruleset = getattr(sc.get_object(User, 'id', path), 'playmode')
    token = sc.get_object(Token, 'user_id', path, as_dict=True)
    sc.direct_update_user(path, token, ruleset)
    sc.update_user_scores(path)"""
    return send_from_directory('../client/public', 'index.html')

@app.route("/profile/static/<path:path>")
def icons(path):
    return send_from_directory('../client/public/static', path)

@app.route("/authorize")
def auth_redirect():
    return jsonify(sc.create_authorization_url())

@app.route("/api/search")
def search():
    return jsonify(sc.select_all(User, as_dict=True))

@app.route("/api/profile/<int:id>/<string:ruleset>")
@app.route("/api/profile/<int:id>")
def fetch_profile(id, ruleset=None):
    print(ruleset)
    if not ruleset:
        ruleset = getattr(sc.get_object(User, 'id', id), 'playmode')
    return jsonify(sc.create_profile(id, ruleset))

@app.route("/callback")
def callback():
    code = request.args.get('code')
    token = sc.fetch_token(code)
    sc.handle_authorization(token)
    return redirect("/")

@app.route("/delete_expired_tokens")
def delete_expired_tokens():
    sc.delete_expired_tokens()
    return redirect("/")

@app.route("/queue_dailies")
def dailies():
    queue_dailies(date.today())
    return redirect("/")

def queue_dailies(date):
    previous_user_objects = sc.select_all(User, sort_by=User.last_updated, as_dict=True)
    interval = (sc.intervals['dailies']['interval'] * sc.intervals['hours_to_seconds']) / len(previous_user_objects)
    total_interval = 0
    for previous_user in previous_user_objects:
        id = previous_user['id']
        token = sc.get_object(Token, 'user_id', id, as_dict=True)
        for ruleset in sc.rulesets:
            if not db.session.query(exists().where(and_(UserDailyStatistics.id == id, UserDailyStatistics.ruleset == ruleset, UserDailyStatistics.start_date == date))).scalar():
                previous_user_ruleset = sc.get_object(sc.tables[ruleset], 'id', id, as_dict=True)
                sc.direct_update_user(id, token, ruleset)
                new_user_ruleset = sc.get_object(sc.tables[ruleset], 'id', id, as_dict=True)
                play_time = new_user_ruleset['play_time'] - previous_user_ruleset['play_time']
                play_count = new_user_ruleset['play_count'] - previous_user_ruleset['play_count']
                note_count = new_user_ruleset['total_hits'] - previous_user_ruleset['total_hits']
                ranked_score = new_user_ruleset['ranked_score'] - previous_user_ruleset['ranked_score']
                total_score = new_user_ruleset['total_score'] - new_user_ruleset['total_score']
                """scheduler.add_job(sc.store_daily_statistics, 'date', run_date=(datetime.now() + timedelta(seconds=10)), args=[id, ruleset, date, play_time, play_count, note_count, ranked_score, total_score])"""
                sc.store_daily_statistics(id, ruleset, date, play_time, play_count, note_count, ranked_score, total_score)
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
    scheduler.start()
    scheduler.add_job(queue_dailies, 'cron', hour=sc.intervals['dailies']['hour'], args=[(date.today() - timedelta(days=1))])
    scheduler.add_job(queue_refresh, 'cron', hour=sc.intervals['refresh']['interval'])
    scheduler.add_job(queue_users, 'cron', hour=sc.intervals['users']['interval'])