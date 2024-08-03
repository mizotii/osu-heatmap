"""for writing to the database"""

from datetime import datetime, timedelta
from db.models import db, User
from config.osu_api import fetch as ft

def store_user(token, user):
    db.session.add(User(
        id=user['id'],
        access_token=token['access_token'],
        expires_at=timedelta(seconds = token['expires_in'])+datetime.now(),
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
        username=user['username']
    ))
    db.session.commit()
    return