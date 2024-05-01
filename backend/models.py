from config import db_config as dc
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Index
from sqlalchemy.orm import relationship
from sqlalchemy.schema import PrimaryKeyConstraint

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

# makes queries JSON serializable
class Class(db.Model):
    __abstract__ = True

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
# for each ruleset of every user
class UserRuleset(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, db.ForeignKey('tokens.user_id'), primary_key=True)
    last_updated = db.Column(db.DateTime)
    username = db.Column(db.String(dc.constraints['max_user_length']))
    # retroactive to first update
    play_count = db.Column(db.Integer)
    play_time = db.Column(db.Integer)
    ranked_score = db.Column(db.BigInteger)
    streak_current = db.Column(db.Integer)
    streak_longest = db.Column(db.Integer)
    total_hits = db.Column(db.BigInteger)
    total_score = db.Column(db.BigInteger)

class User(Class):
    __tablename__ = 'users'

    avatar_url = db.Column(db.String(dc.constraints['long']))
    country_code = db.Column(db.String(dc.constraints['short']))
    cover_url = db.Column(db.String(dc.constraints['long']))
    id = db.Column(db.Integer, db.ForeignKey('tokens.user_id'), primary_key=True)
    is_deleted = db.Column(db.Boolean)
    is_restricted = db.Column(db.Boolean)
    last_updated = db.Column(db.DateTime)
    username = db.Column(db.String(dc.constraints['max_user_length']))

class UserDailyStatistics(Class):
    __tablename__ = 'daily_statistics'

    id = db.Column(db.Integer, db.ForeignKey('tokens.user_id'), primary_key=True)
    ruleset = db.Column(db.String(dc.constraints['short']))
    start_date = db.Column(db.DateTime)
    playtime = db.Column(db.Interval)
    playcount = db.Column(db.Integer)
    notecount = db.Column(db.Integer)

class UserOsu(UserRuleset):
    __tablename__ = 'users_osu'

class UserTaiko(UserRuleset):
    __tablename__ = 'users_taiko'

class UserCatch(UserRuleset):
    __tablename__ = 'users_catch'

class UserMania(UserRuleset):
    __tablename__ = 'users_mania'

class Token(Class):
    __tablename__ = 'tokens'

    user_id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(dc.constraints['max_token_length']))
    expires_at = db.Column(db.DateTime)
    refresh_token = db.Column(db.String(dc.constraints['max_token_length']))
    token_type = db.Column(db.String(dc.constraints['veryshort']))

class BeatmapSet(Class):
    __tablename__ = 'beatmapsets'

    id = db.Column(db.Integer, primary_key=True)
    card = db.Column(db.String(dc.constraints['long']))
    card_2x = db.Column(db.String(dc.constraints['long']))
    creator = db.Column(db.String(dc.constraints['max_user_length']))
    creator_id = db.Column(db.Integer)
    difficulty_rating = db.Column(db.Float)
    mode = db.Column(db.String(dc.constraints['short']))
    status = db.Column(db.String(dc.constraints['short']))
    title = db.Column(db.String(dc.constraints['long']))
    title_unicode = db.Column(db.String(dc.constraints['long']))
    total_length = db.Column(db.Integer)

    beatmap = relationship('Beatmap', back_populates='beatmapset')

class Beatmap(Class):
    __tablename__ = 'beatmaps'

    beatmapset_id = db.Column(db.Integer, db.ForeignKey('beatmapsets.id'), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(dc.constraints['long']))

    beatmapset = relationship('BeatmapSet', back_populates='beatmap')

    __table_args__ = (
        PrimaryKeyConstraint('beatmapset_id', 'id', name='pk_beatmap'),
        Index('ix_beatmaps_id', 'id')
    )

class Score(Class):
    __tablename__ = 'scores'

    id = db.Column(db.String(dc.constraints['veryshort']), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('tokens.user_id'))
    timestamp = db.Column(db.DateTime)
    mode = db.Column(db.String(dc.constraints['veryshort']))
    count_300 = db.Column(db.Integer)
    count_100 = db.Column(db.Integer)
    count_50 = db.Column(db.Integer)
    count_geki = db.Column(db.Integer)
    count_katu = db.Column(db.Integer)
    count_miss = db.Column(db.Integer)
    notes = db.Column(db.Integer)
    # display
    accuracy = db.Column(db.Float)
    beatmap_id = db.Column(db.Integer, db.ForeignKey('beatmaps.id'))
    beatmapset_id = db.Column(db.Integer, db.ForeignKey('beatmapsets.id'))
    max_combo = db.Column(db.Integer)
    mods = db.Column(db.String(dc.constraints['veryshort']))
    passed = db.Column(db.Boolean)
    rank = db.Column(db.String(dc.constraints['veryshort']))
