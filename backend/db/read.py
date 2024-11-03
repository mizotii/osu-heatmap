"""for reading from the database"""
from config.server_config import daily_statistics
from db.models import db, ClientCredentialsKey, User, UserDailyStatistics, Score, Beatmap, BeatmapSet
from config import server_config as sc
from datetime import timedelta
from sqlalchemy import and_, between, desc, func

def read_user(id):
    user = User.query.filter_by(id=id).first()
    return user

def read_ruleset(id, ruleset):
    user = sc.ruleset_tables[ruleset].query.filter_by(id=id).first()
    return user

def read_cell(id, ruleset, date):
    cell = UserDailyStatistics.query.filter_by(id=id, ruleset=ruleset, start_date=date).first()
    return cell

# optimizable: query all statistics at once
def read_max_statistic(id, ruleset):
    data = {}
    for statistic in daily_statistics:
        max = db.session.query(func.max(daily_statistics[statistic])).\
            filter(
                and_(
                    UserDailyStatistics.id == id,
                    UserDailyStatistics.ruleset == ruleset,
                )
            ).scalar()
        data[statistic] = max
    return data

def read_beatmap(id, set_id):
    beatmap = Beatmap.query.filter_by(id=id, beatmapset_id=set_id).first()
    return beatmap

def read_beatmapset(id):
    beatmapset = BeatmapSet.query.filter_by(id=id).first()
    return beatmapset

def read_score(user_id, timestamp):
    score = Score.query.filter_by(user_id=user_id, timestamp=timestamp).first()
    return score

def read_user_count():
    return db.session.query(func.count(User.id)).scalar()

def read_client_credentials():
    return ClientCredentialsKey.query.first()

# optimizable: query all statistics at once
def read_summed_statistic(id, date, statistic):
    sum = db.session.query(func.sum(daily_statistics[statistic])).\
        filter(
            and_(
                UserDailyStatistics.id == id,
                UserDailyStatistics.start_date == date,
            )
        ).scalar()
    return sum

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