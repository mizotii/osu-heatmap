import dateutil.parser
import os
import pydash as _
import requests
import time
from datetime import datetime, timedelta
from models import db, Class, Score, Token, User, UserCatch, UserMania, UserOsu, UserTaiko
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
        'fruits': '/me/fruits',
        'mania': '/me/mania',
    },
    'token': 'https://osu.ppy.sh/oauth/token',
}

rulesets = [
    'fruits', 'mania', 'osu', 'taiko', 
]

tables = {
    'fruits': UserCatch,
    'mania': UserMania,
    'osu': UserOsu,
    'taiko': UserTaiko,
}

token_attributes = {
    'access_token': 'access_token',
    'expires_at': 'expires_in',
    'refresh_token': 'refresh_token',
    'token_type': 'token_type',
}

user_attributes = {
    'avatar_url': 'avatar_url',
    'country_code': 'country_code',
    'cover_url': 'cover.url',
    'id': 'id',
    'is_deleted': 'is_deleted',
    'is_restricted': 'is_restricted',
    'play_count': 'statistics.play_count',
    'play_time': 'statistics.play_time',
    'ranked_score': 'statistics.ranked_score',
    'total_hits': 'statistics.total_hits',
    'total_score': 'statistics.total_score',
    'username': 'username',
}

# requires above config

authorization_parameters = {
    'client_id': client_credentials['client_id'],
    'redirect_uri': endpoints['callback'],
    'response_type': 'code',
    'scope': 'public identify',
    'state': 'randomval',
}

def after_authorization(token, code):
    id = fetch_user(token['access_token'], attribute='id')
    hyp_user = get_object(Token, 'user_id', id)

    # schema draws Token as parent class, meaning if a Token exists, so does its User in all facets
    if hyp_user:
        refresh_token(hyp_user, code)
        for ruleset in rulesets:
            direct_update_user(id, token, ruleset)
    else:
        store_token(id, token)
        store_user(token)
        for ruleset in rulesets:
            store_user_ruleset(token, ruleset)

def create_authorization_url():
    return urljoin(endpoints['authorize'], '?' + urlencode(authorization_parameters))

def calculate_expiration(interval):
    return (datetime.now() + timedelta(seconds=interval))

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

def create_refresh_parameters(refresh):
    if not refresh:
        raise ValueError('could not create refresh token parameters: no refresh token provided')
    params = {
        'client_id': client_credentials['client_id'],
        'client_secret': client_credentials['client_secret'],
        'grant_type': 'refresh_token',
        'refresh_token': refresh,
        'scope': 'public identify',
    }
    return params

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

# updates general user and osu ruleset for user by default (osu)
def direct_update_user(id, token, ruleset):
    if ruleset == 'osu':
        table = User
        old_user = get_object(table, 'id', id)
        new_user = fetch_user(token['access_token'])
        update_user(table, old_user, new_user)
    table = tables[ruleset]
    old_user = get_object(table, 'id', id)
    new_user = fetch_user(token['access_token'], ruleset)
    update_user(table, old_user, new_user)

def fetch_token(code):
    response = requests.post(
        endpoints['token'],
        headers=create_headers(),
        data=create_token_parameters(code)
    )
    return response.json()

def fetch_user(access, ruleset='osu', attribute=None):
    if ruleset not in rulesets:
        raise ValueError(write_value_error(ruleset, rulesets))
    response = requests.get(
        endpoints['api'] + endpoints['this_user'][ruleset],
        headers=create_headers(access)
    )
    data = response.json()
    if attribute:
        if attribute not in user_attributes:
            raise ValueError(write_value_error(attribute, user_attributes))
        return _.get(data, user_attributes[attribute])
    return data

def get_object(table, attribute, value, check_exists_only=False, as_dict=False):
    valid_attributes = table.__table__.columns.keys()
    if attribute not in valid_attributes:
        raise ValueError(write_value_error(attribute, valid_attributes))
    if check_exists_only:
        return db.session.query(exists().where(getattr(table, attribute) == value)).scalar()
    else:
        query = (db.session.query(table).where(getattr(table, attribute) == value).first())
        if not as_dict:
            return query
        else:
            return query.as_dict()

def hard_refresh_token(attribute, value, code):
    if code is None:
        raise ValueError('could not hard refresh token: no code provided')
    old_token = get_object(Token, attribute, value)
    new_token = fetch_token(code)
    for key in Token.__table__.columns.keys():
        if key not in ('user_id', 'expires_at'):
            setattr(old_token, key, _.get(new_token, user_attributes[key]))
    setattr(old_token, 'expires_at', calculate_expiration(new_token['expires_in']))

def refresh_token(user, code=None):
    if getattr(user, 'expires_at') > datetime.now():
        return 'token is still valid!'
    refresh = getattr(user, 'refresh_token')
    response = requests.post(
        endpoints['token'],
        headers=create_headers(),
        data=create_refresh_parameters(refresh)
    )
    data = response.json()
    if 'error' in data:
        hard_refresh_token('refresh_token', refresh, code)
        desc = data['error_description']
        hint = data['hint']
        raise ValueError(f'error description: {desc} hint: {hint}')
    for key in Token.__table__.columns.keys():
        if key not in ('user_id', 'expires_at'):
            setattr(user, key, _.get(data, user_attributes[key]))
    setattr(user, 'expires_at', calculate_expiration(data['expires_in']))

# stores token, then stores all four user rulesets
def store_token(id, token):
    db.session.add(
        Token(
            user_id=id,
            access_token=token['access_token'],
            expires_at=(calculate_expiration(token['expires_in'])),
            refresh_token=token['refresh_token'],
            token_type=token['token_type'],
        )
    )
    db.session.commit()

# todo: rework a la update functions
def store_user(token):
    user = fetch_user(token['access_token'])
    db.session.add(
        User(
            avatar_url=_.get(user, user_attributes['avatar_url']),
            country_code=_.get(user, user_attributes['country_code']),
            cover_url=_.get(user, user_attributes['cover_url']),
            id=_.get(user, user_attributes['id']),
            is_deleted=_.get(user, user_attributes['is_deleted']),
            is_restricted=_.get(user, user_attributes['is_restricted']),
            last_updated=datetime.now(),
            username=_.get(user, user_attributes['username']),
        )
    )
    db.session.commit()

def store_user_ruleset(token, ruleset):
    user_ruleset = fetch_user(token['access_token'], ruleset)
    db.session.add(
        tables[ruleset](
            id=_.get(user_ruleset, user_attributes['id']),
            last_updated=datetime.now(),
            username=_.get(user_ruleset, user_attributes['username']),
            play_count=_.get(user_ruleset, user_attributes['play_count']),
            play_time=_.get(user_ruleset, user_attributes['play_time']),
            ranked_score=_.get(user_ruleset, user_attributes['ranked_score']),
            streak_current=0,
            streak_longest=0,
            total_hits=_.get(user_ruleset, user_attributes['total_hits']),
            total_score=_.get(user_ruleset, user_attributes['total_score']),
        )
    )
    db.session.commit()

def update_user(table, old_user, new_user):
    for key in table.__table__.columns.keys():
        if key not in ('id', 'last_updated', 'streak_current', 'streak_longest'):
            print(key)
            print(old_user, key, _.get(new_user, user_attributes[key]))
            setattr(old_user, key, _.get(new_user, user_attributes[key]))
    setattr(old_user, 'last_updated', datetime.now())

def write_value_error(invalid, valid):
    valid_types = ', '.join(valid)
    return f'invalid type \'{invalid}. valid types: {valid_types}.'