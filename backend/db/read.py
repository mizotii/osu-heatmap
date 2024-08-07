"""for reading from the database"""
from db.models import db, User, UserOsu, UserTaiko, UserCatch, UserMania, UserDailyStatistics, Score, Beatmap, BeatmapSet
from config import server_config as sc
from datetime import timedelta
from sqlalchemy import and_, between, desc, exists

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

def all_scores_on_day(id, ruleset, timestamp):
    scores = db.session.query(Score, Beatmap, BeatmapSet).\
        where(
            and_(
                Score.user_id == id,
                Score.ruleset == ruleset,
                between(Score.timestamp, timestamp, timestamp + timedelta(days=1)),
            )
        ).\
        where(Score.beatmap_id == Beatmap.id).\
        where(Beatmap.beatmapset_id == BeatmapSet.id).\
        order_by(desc(Score.timestamp)).\
        all()
    return scores

def all_users(app):
    with app.app_context():
        return User.query.all()
    
def all_cells_for_user(id, ruleset):
    return UserDailyStatistics.query.filter_by(id=id, ruleset=ruleset).all()