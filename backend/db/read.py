"""for reading from the database"""
from db.models import db, User, UserOsu, UserTaiko, UserCatch, UserMania, UserDailyStatistics, Score, Beatmap, BeatmapSet
from config import server_config as sc

def read_user(id):
    user = User.query.filter_by(id=id).first()
    return user

def read_ruleset(id, ruleset):
    user = sc.ruleset_tables[ruleset].query.filter_by(id=id).first()
    return user

def read_cell(id, ruleset, date):
    cell = UserDailyStatistics.query.filter_by(id=id, ruleset=ruleset, start_date=date).first()
    return cell

def read_beatmap(id, set_id):
    beatmap = Beatmap.query.filter_by(id=id, beatmapset_id=set_id).first()
    return beatmap

def read_beatmapset(id):
    beatmapset = BeatmapSet.query.filter_by(id=id).first()
    return beatmapset

def read_score(id):
    score = Score.query.filter_by(id=id).first()
    return score

def all_users(app):
    with app.app_context():
        return User.query.all()