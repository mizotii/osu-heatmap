from config.server_config import credentials, endpoints, headers
from datetime import datetime, timedelta
from db.models import db
import requests

def refresh_token(app, user):
    with app.app_context():
        url = endpoints['token']
        payload = {
            'client_id': credentials['client_id'],
            'client_secret': credentials['client_secret'],
            'grant_type': 'refresh_token',
            'refresh_token': user.__dict__['refresh_token'],
        }
        r = requests.post(url=url, headers=headers, params=payload).json()
        setattr(user, 'access_token', r['access_token'])
        setattr(user, 'expires_at', timedelta(seconds = r['expires_in']) + datetime.now())
        setattr(user, 'refresh_token', r['refresh_token'])
        db.session.commit()