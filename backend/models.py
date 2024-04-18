from config import constraints
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(constraints['MAX_USER_LENGTH']))
    global_rank = db.Column(db.Integer)
    access = db.Column(db.String(constraints['MAX_TOKEN_LENGTH']))
    expires = db.Column(db.Integer)
    refresh = db.Column(db.String(constraints['MAX_TOKEN_LENGTH']))
    type = db.Column(db.String(constraints['MAX_TYPE_LENGTH']))

class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(DateTime)
    notes = db.Column(db.Integer)
    accuracy = db.Column(db.Float)
    # other stats like 300s 100s 50s misses score rank etc
    