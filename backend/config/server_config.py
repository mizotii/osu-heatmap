import dateutil.parser
import os
import pydash as _
import requests
import time
from datetime import datetime, timedelta
from models import db, Class, Score, Token, User
from sqlalchemy import exists, func
from urllib.parse import urlencode, urljoin

client_credentials = {
    'client_id': os.environ['CLIENT_ID'],
    'client_secret': os.environ['CLIENT_SECRET'],
}

database = {
    'db_uri': os.environ['DB_URI'],
}

endpoints = {
    'authorize': 'https://osu.ppy.sh/oauth/authorize',
    'api': 'https://osu.ppy.sh/api/v2',
    'callback': 'http://localhost:5000/callback',
    'this_user': {
        'osu': '/me',
        'taiko': '/me/taiko',
        'fruits': '/me/catch',
        'mania': '/me/mania',
    },
    'token': 'https://osu.ppy.sh/oauth/token',
}

rulesets = [
    'osu', 'taiko', 'fruits', 'mania'
]

# requires above config

authorization_parameters = {
    'client_id': client_credentials['client_id'],
    'redirect_uri': endpoints['callback'],
    'response_type': 'code',
    'scope': 'public identify',
    'state': 'randomval',
}

def create_authorization_url():
    return urljoin(endpoints['authorize'], '?' + urlencode(authorization_parameters))

def create_headers(token=None):
    headers = {
        'Accept': 'application/json',
    }
    if token:
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = f'Bearer {token}'
    else:
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
    return headers

def create_token_parameters(code):
    if not code:
        raise ValueError('could not create token parameters: no code provided')
    params = {
        'client_id': client_credentials['client_id'],
        'client_secret': client_credentials['client_secret'],
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': endpoints['callback'],
    }
    return params

def fetch_token(code):
    response = requests.post(
        endpoints['BASE_URL'] + endpoints['TOKEN'],
        headers=create_headers(),
        data=create_token_parameters(code)
    )
    return response.json()

def fetch_user(token, ruleset):
    if ruleset not in rulesets:
        raise ValueError(write_value_error(ruleset, rulesets))
    response = requests.post(
        endpoints['api'] + endpoints['this_user'][ruleset],
        headers=create_headers(token['access_token'])
    )
    return response.json()

# TODO
def store_token(token):
    user = fetch_user(token)

def store_user(user):
    return

def write_value_error(invalid, valid):
    valid_types = ', '.join(valid)
    return f'invalid type \'{invalid}. valid types: {valid_types}.'