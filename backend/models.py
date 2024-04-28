from config import db_config as dc
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

# makes queries JSON serializable
class Class(db.Model):
    __abstract__ = True

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class User(Class):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(dc.constraints['MAX_USER_LENGTH']))
    global_rank = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime)

class Token(Class):
    __tablename__ = 'tokens'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    access_token = db.Column(db.String(dc.constraints['MAX_TOKEN_LENGTH']), nullable=False)
    expires_at = db.Column(db.DateTime)
    refresh_token = db.Column(db.String(dc.constraints['MAX_TOKEN_LENGTH']), nullable=False)
    token_type = db.Column(db.String(dc.constraints['MAX_TYPE_LENGTH']), nullable=False)

class Score(Class):
    __tablename__ = 'scores'

    id = db.Column(db.String(dc.constraints['MAX_SCORE_LENGTH']), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    playtime = db.Column(db.Interval)
    mode = db.Column(db.String(dc.constraints['MAX_MODE_LENGTH']))
    count_300 = db.Column(db.Integer)
    count_100 = db.Column(db.Integer)
    count_50 = db.Column(db.Integer)
    count_geki = db.Column(db.Integer)
    count_katu = db.Column(db.Integer)
    count_miss = db.Column(db.Integer)
    notes = db.Column(db.Integer, nullable=False)
    # for display purposes
    accuracy = db.Column(db.Float, nullable=False)
    max_combo = db.Column(db.Integer)
    # need: mods (int bitset?)
    