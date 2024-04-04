import os
import requests
from models import db, User
from urllib.parse import urlencode, urljoin

client_credentials = {
    'CLIENT_ID': os.environ.get('CLIENT_ID'),
    'CLIENT_SECRET': os.environ.get('CLIENT_SECRET'),
}

constraints = {
    'MAX_USER_LENGTH': 15
}

database = {
    'DB_URI': os.environ.get('DB_URI'),
}

endpoints = {
    'BASE_URL': 'https://osu.ppy.sh/',
    'REDIRECT_URI': 'http://localhost:5000/callback',
    'AUTHORIZATION': 'oauth/authorize',
    'TOKEN': 'oauth/token',
    'THIS_USER': '/api/v2/me/',
}

def create_auth_url():
    payload = {
        'client_id': client_credentials['CLIENT_ID'],
        'redirect_uri': endpoints['REDIRECT_URI'],
        'response_type': 'code',
        'scope': 'public identify',
        'state': 'randomval',
    }
    query = urlencode(payload)
    url = urljoin(endpoints['BASE_URL'] + endpoints['AUTHORIZATION'], '?' + query)
    return url

def get_headers(token=None):
    headers =  {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    if token:
        headers['Authorization'] = f'Bearer {token}'
    return headers

def get_this_user(access_token):
    headers=get_headers(access_token)
    response = requests.get(endpoints['BASE_URL'] + endpoints['THIS_USER'], headers=get_headers(access_token))
    return response.json()

def get_token_data(code):
    payload = {
        'client_id': client_credentials['CLIENT_ID'],
        'client_secret': client_credentials['CLIENT_SECRET'],
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': endpoints['REDIRECT_URI'],
    }
    response = requests.post(endpoints['BASE_URL'] + endpoints['TOKEN'], headers=get_headers(), data=payload)
    return response.json()
    
def store_token(token_data):
    access_token = token_data['access_token']
    user = get_this_user(access_token)
    db.session.add(
        User(
            id=user.get('id'),
            name=user.get('username'),
            access=access_token,
            expires=token_data['expires_in'],
            refresh=token_data['refresh_token'],
            type=token_data['token_type']
        )
    )
    return