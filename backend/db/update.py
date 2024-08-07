"""for writing to the database"""

from datetime import date, datetime, timedelta
from db.models import db, User, UserOsu, UserTaiko, UserCatch, UserMania, UserDailyStatistics
from config.osu_api import fetch as ft
from config import server_config as sc
import read as rd

user_ruleset_attributes = [
    'last_updated',
    'username',
]

def store_user(token, user):
    db.session.add(User(
        id=user['id'],
        access_token=token['access_token'],
        expires_at=timedelta(seconds=token['expires_in'])+datetime.now(),
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],

        avatar_url=user['avatar_url'],
        country_code=user['country_code'],
        cover_url=user['cover']['url'],
        is_deleted=user['is_deleted'],
        is_restricted=user['is_restricted'],
        last_updated=datetime.now(),
        playmode=user['playmode'],
        registration_date=datetime.now(),
        username=user['username'],
    ))
    db.session.commit()

def store_user_ruleset(data, ruleset, id):
    db.session.add(sc.ruleset_tables[ruleset](
        id=id,
        last_updated=datetime.now(),
        username=data['username'],
        play_count=data['play_count'],
        play_time=data['play_time'],
        ranked_score=data['ranked_score'],
        streak_current=0,
        streak_longest=0,
        total_hits=data['total_hits'],
        total_score=data['total_score'],
    ))
    db.session.commit()

def store_user_daily(ruleset, id):
    db.session.add(UserDailyStatistics(
        id=id,
        ruleset=ruleset,
        start_date=datetime.date.today(),
        play_time=0,
        play_count=0,
        note_count=0,
        ranked_score=0,
        total_score=0,
    ))
    db.session.commit()

def update_user_statistics(app, user, ruleset):
    with app.app_context():

        updated_ruleset = ft.fetch_user(user.__dict__['access_token'], ruleset).__dict__
        id = updated_ruleset['id']
        old_ruleset = rd.read_ruleset(id, ruleset)

        if not old_ruleset:
            store_user_ruleset(updated_ruleset, ruleset, id)
            store_user_daily(ruleset, id)
        else:

            # heatmap cell
            
            old_cell = rd.read_cell(id, ruleset, datetime.date.today())
            if not old_cell:
                store_user_daily(ruleset, id)
            else:
                setattr(old_cell, 'play_time', updated_ruleset['play_time'] - old_ruleset.__dict__['play_time'])
                setattr(old_cell, 'play_count', updated_ruleset['play_count'] - old_ruleset.__dict__['play_count'])
                setattr(old_cell, 'note_count', updated_ruleset['note_count'] - old_ruleset.__dict__['note_count'])
                setattr(old_cell, 'ranked_score', updated_ruleset['ranked_score'] - old_ruleset.__dict__['ranked_score'])
                setattr(old_cell, 'total_score', updated_ruleset['total_score'] - old_ruleset.__dict__['total_score'])

            # todo: update ruleset attributes for everything except streaks using collection above
            
            # ruleset

            setattr(old_ruleset, 'last_updated', datetime.now())
            setattr(old_ruleset, 'username', updated_ruleset['username'])
            setattr(old_ruleset, 'play_count', updated_ruleset['play_count'])
            setattr(old_ruleset, 'play_time', updated_ruleset['play_time'])
            setattr(old_ruleset, 'ranked_score', updated_ruleset['ranked_score'])
            setattr(old_ruleset, 'total_hits', updated_ruleset['total_hits'])
            setattr(old_ruleset, 'total_score', updated_ruleset['total_score'])

            # maybe cycle through rulesets here, so as not to commit 4 times?
            db.session.commit()
