"""for reading from the database"""
from db.models import db, User, UserOsu, UserTaiko, UserCatch, UserMania, UserDailyStatistics

ruleset_tables = {
    'osu': UserOsu,
    'taiko': UserTaiko,
    'catch': UserCatch,
    'mania': UserMania,
}

def read_user(id):
    user = User.query.filter_by(id=id).first()
    return user

def read_ruleset(id, ruleset):
    user = ruleset_tables[ruleset].query.filter_by(id=id).first()
    return user

def read_cell(id, ruleset, date):
    cell = UserDailyStatistics.query.filter_by(id=id, ruleset=ruleset, start_date=date).first()
    return cell

def all_users(app):
    with app.app_context():
        return User.query.all()