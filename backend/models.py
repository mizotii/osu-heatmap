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

class Token(Class):
    __tablename__ = 'tokens'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    access_token = db.Column(db.String(dc.constraints['MAX_TOKEN_LENGTH']), nullable=False)
    expires_in = db.Column(db.Integer)
    refresh_token = db.Column(db.String(dc.constraints['MAX_TOKEN_LENGTH']), nullable=False)
    token_type = db.Column(db.String(dc.constraints['MAX_TYPE_LENGTH']), nullable=False)

class Score(Class):
    __tablename__ = 'scores'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(DateTime, nullable=False)
    notes = db.Column(db.Integer, nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    # other stats like 300s 100s 50s misses score rank etc
    