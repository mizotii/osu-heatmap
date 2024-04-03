from config import constraints
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(constraints['MAX_USER_LENGTH']))
    access = db.Column(db.String, primary_key=True)
    expires = db.Column(db.Integer)
    refresh = db.Column(db.String)
    type = db.Column(db.String)

class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(DateTime)
    accuracy = db.Column(db.Float)