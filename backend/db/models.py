from db import db_config as dc
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Index
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
    
class ClientCredentialsKey(Class):
    __tablename__ = 'client_key'

    access_token = db.Column(db.String(dc.constraints['max_token_length']))
    expires_at = db.Column(db.DateTime)
    token_type = db.Column(db.String(dc.constraints['veryshort']), primary_key=True)
    
# for each ruleset of every user
class UserRuleset(db.Model):
    __abstract__ = True

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    last_updated = db.Column(db.DateTime)
    username = db.Column(db.String(dc.constraints['max_user_length']))
    # retroactive to first update (since {registration_date})
    accumulated_play_count = db.Column(db.Integer)
    accumulated_play_time = db.Column(db.Integer)
    accumulated_total_hits = db.Column(db.BigInteger)
    accumulated_ranked_score = db.Column(db.BigInteger)
    accumulated_total_score = db.Column(db.BigInteger)

    # stats displayed on main profile
    play_count = db.Column(db.Integer)
    play_time = db.Column(db.Integer)
    total_hits = db.Column(db.BigInteger)
    ranked_score = db.Column(db.BigInteger)
    total_score = db.Column(db.BigInteger)

    streak_current = db.Column(db.Integer)
    streak_longest = db.Column(db.Integer)

class UserDailyStatistics(Class):
    __tablename__ = 'daily_statistics'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    ruleset = db.Column(db.String(dc.constraints['short']), primary_key=True)
    start_date = db.Column(db.DateTime, primary_key=True)
    play_time = db.Column(db.Integer)
    play_count = db.Column(db.Integer)
    total_hits = db.Column(db.Integer)
    ranked_score = db.Column(db.Integer)
    streak_counted = db.Column(db.Boolean)
    total_score = db.Column(db.Integer)

    __table_args__ = (
        PrimaryKeyConstraint('id', 'ruleset', 'start_date', name='daily_statistics_pk'),
    )

class UserOsu(UserRuleset):
    __tablename__ = 'users_osu'

class UserTaiko(UserRuleset):
    __tablename__ = 'users_taiko'

class UserCatch(UserRuleset):
    __tablename__ = 'users_catch'

class UserMania(UserRuleset):
    __tablename__ = 'users_mania'

class User(UserMixin, Class):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(dc.constraints['max_token_length']))
    token_type = db.Column(db.String(dc.constraints['veryshort']))

    avatar_url = db.Column(db.String(dc.constraints['long']))
    country_code = db.Column(db.String(dc.constraints['short']))
    cover_url = db.Column(db.String(dc.constraints['long']))
    is_deleted = db.Column(db.Boolean)
    last_updated = db.Column(db.DateTime)
    playmode = db.Column(db.String(dc.constraints['short']))
    registration_date = db.Column(db.DateTime)
    username = db.Column(db.String(dc.constraints['max_user_length']))

    streak_current = db.Column(db.Integer)
    streak_longest = db.Column(db.Integer)
    streak_counted = db.Column(db.Boolean)

    def get_id(self):
        return str(self.id)

class BeatmapSet(Class):
    __tablename__ = 'beatmapsets'

    artist = db.Column(db.String(dc.constraints['long']))
    artist_unicode = db.Column(db.String(dc.constraints['long']))
    id = db.Column(db.Integer, primary_key=True)
    creator = db.Column(db.String(dc.constraints['max_user_length']))
    creator_id = db.Column(db.Integer)
    slimcover = db.Column(db.String(dc.constraints['long']))
    slimcover_2x = db.Column(db.String(dc.constraints['long']))
    status = db.Column(db.String(dc.constraints['short']))
    title = db.Column(db.String(dc.constraints['long']))
    title_unicode = db.Column(db.String(dc.constraints['long']))

    beatmap = relationship('Beatmap', back_populates='beatmapset')

class Beatmap(Class):
    __tablename__ = 'beatmaps'

    beatmapset_id = db.Column(db.Integer, db.ForeignKey('beatmapsets.id'), primary_key=True)
    difficulty_rating = db.Column(db.Float)
    id = db.Column(db.Integer, primary_key=True)
    ruleset = db.Column(db.String(dc.constraints['short']))
    total_length = db.Column(db.Integer)
    version = db.Column(db.String(dc.constraints['long']))

    beatmapset = relationship('BeatmapSet', back_populates='beatmap')

    __table_args__ = (
        PrimaryKeyConstraint('beatmapset_id', 'id', name='pk_beatmap'),
        Index('ix_beatmaps_id', 'id')
    )

class Score(Class):
    __tablename__ = 'scores'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, primary_key=True)
    ruleset = db.Column(db.String(dc.constraints['veryshort']))
    count_300 = db.Column(db.Integer)
    count_100 = db.Column(db.Integer)
    count_50 = db.Column(db.Integer)
    count_geki = db.Column(db.Integer)
    count_katu = db.Column(db.Integer)
    count_miss = db.Column(db.Integer)
    notes = db.Column(db.Integer)
    # display
    accuracy = db.Column(db.String(dc.constraints['veryshort']))
    beatmap_id = db.Column(db.Integer, db.ForeignKey('beatmaps.id'))
    beatmapset_id = db.Column(db.Integer, db.ForeignKey('beatmapsets.id'))
    max_combo = db.Column(db.Integer)
    mods = db.Column(db.String(dc.constraints['veryshort']))
    passed = db.Column(db.Boolean)
    rank = db.Column(db.String(dc.constraints['veryshort']))
    score = db.Column(db.Integer)

    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'timestamp', name='scores_pk'),
    )
