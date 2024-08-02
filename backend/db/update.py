"""for writing to the database"""

from datetime import datetime, timedelta
from db.models import db, Token
from config.osu_api import fetch as ft

def store_token(token, id):
    db.session.add(Token(
        user_id=id,
        access_token=token['access_token'],
        expires_at=timedelta(seconds = token['expires_in'])+datetime.now(),
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],
    ))
    db.session.commit()
    return