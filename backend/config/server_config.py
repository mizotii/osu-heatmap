import dateutil.parser
import os
import pydash as _
import requests
from datetime import datetime, timedelta
from models import db, Class, Score, Token, User
from sqlalchemy import exists, func
from urllib.parse import urlencode, urljoin

automatic_intervals = {
    'REFRESH_TOKEN': '43200',
    'REFRESH_PROFILE': '7200',
}

client_credentials = {
    'CLIENT_ID': os.environ['CLIENT_ID'],
    'CLIENT_SECRET': os.environ['CLIENT_SECRET'],
}

database = {
    'DB_URI': os.environ['DB_URI'],
}

endpoints = {
    'AUTHORIZATION': '/oauth/authorize',
    'BASE_URL': 'https://osu.ppy.sh',
    'REDIRECT_URI': 'http://localhost:5000/callback',
    'THIS_USER': '/me',
    'TOKEN': '/oauth/token',
    'V2': '/api/v2',
}

errors = {
    'USER_NOT_FOUND': 'user not found!',
}

fetch_token_payload = {
    'client_id': client_credentials['CLIENT_ID'],
    'client_secret': client_credentials['CLIENT_SECRET'],
    'code': None,
    'grant_type': 'authorization_code',
    'redirect_uri': endpoints['REDIRECT_URI'],
}

profile_data = {
    'USERNAME': None,
    'GLOBAL_RANK': None,
    'SCORES': {},
}

score_attributes = {
    'id': 'current_user_attributes.pin.score_id',
    'user_id': 'user.id',
    'timestamp': 'created_at',
    'count_300': 'statistics.count_300',
    'count_100': 'statistics.count_100',
    'count_50': 'statistics.count_50',
    'accuracy': 'accuracy',
    }

score_parameters = {
    'scope': 'public',
    'include_fails': '1',
    'mode': 'osu',
}

token_attributes = {
    'user_id': 'user_id',
    'access_token': 'access_token',
    'expires_in': 'expires_at',
    'refresh_token': 'refresh_token',
    'token_type': 'token_type',
}

user_attributes = {
    'id': 'id',
    'name': 'username',
    'global_rank': 'statistics.global_rank',
}

user_search = {
    'USER_FOUND': False,
    'USER_ID': None,
}

authentication_payload = {
    'client_id': client_credentials['CLIENT_ID'],
    'redirect_uri': endpoints['REDIRECT_URI'],
    'response_type': 'code',
    'scope': 'public identify',
    'state': 'randomval',
}

def create_auth_url():
    query = urlencode(authentication_payload)
    url = urljoin(endpoints['BASE_URL'] + endpoints['AUTHORIZATION'], '?' + query)
    return url

def get_expiration(interval):
    return (datetime.now() + timedelta(seconds=interval))

def get_headers(token=None):
    headers = {
        'Accept': 'application/json',
    }
    if token:
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = f'Bearer {token}'
    else:
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
    return headers

def get_refresh_payload(refresh):
    payload = {
        'client_id': client_credentials['CLIENT_ID'],
        'client_secret': client_credentials['CLIENT_SECRET'],
        'grant_type': 'refresh_token',
        'refresh_token': refresh,
        'scope': 'public identify',
    }
    return payload

def get_token_data(code):
    response = requests.post(
        endpoints['BASE_URL'] + endpoints['TOKEN'],
        headers=get_headers(),
        data=get_token_payload(code)
    )
    return response.json()

def get_token_payload(code):
    payload = {
        'client_id': client_credentials['CLIENT_ID'],
        'client_secret': client_credentials['CLIENT_SECRET'],
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': endpoints['REDIRECT_URI'],
    }
    return payload

# my bad
def get_user_in(operation_type, token_data):
    valid_operations = ['refresh', 'update']
    if operation_type not in valid_operations:
        raise ValueError(write_value_error(operation_type, valid_operations))
    
    access = token_data['access_token']
    refresh = token_data['refresh_token']

    # creates a new user if they aren't found, updates an old user if they are
    if operation_type == 'update':
        response = requests.get(
            endpoints['BASE_URL'] + endpoints['V2'] + endpoints['THIS_USER'],
            headers=get_headers(access)
        )
        new_user_data = response.json()
        new_user_id = new_user_data['id']

        # if user exists
        if get_user_out('id', new_user_id, True):
            old_user_data = get_user_out('id', new_user_id, False)
            for key in User.__table__.columns.keys():
                if key not in ('id', 'last_updated'):
                    old_user_data[key] = _.get(new_user_data, user_attributes[key])
            old_user_data['last_updated'] = datetime.now()

        # if user is new
        else:
            db.session.add(
                User(
                    id=new_user_id,
                    name=new_user_data[user_attributes['name']],
                    global_rank=_.get(new_user_data, user_attributes['global_rank']),
                    last_updated=datetime.now(),
                )
            )
        
        # rare case where user exists but token doesn't
        if not get_token_out('user_id', new_user_id, True):
            db.session.add(                
                Token(
                    user_id=new_user_id,
                    access_token=access,
                    expires_at=get_expiration(int(token_data['expires_in'])),
                    refresh_token=refresh,
                    token_type=token_data['token_type'],
                )
            )

        # update scores regardless
        store_recent_scores(new_user_id)
        

    # refreshes token
    else:
        old_token = get_token_out('access_token', access, False)
        new_token = refresh_token(refresh)
        for key in Token.__table__.columns.keys():
            if key != 'user_id':
                old_token[key] = _.get(new_token, token_attributes[key])
    
    db.session.commit()

# functions as a user presence checker if last arg is True
def get_object_out(table, attribute, value, check_presence_only=None):
    valid_attributes = table.__table__.columns.keys()
    if attribute not in valid_attributes:
        raise ValueError(write_value_error(attribute, valid_attributes))
    if check_presence_only:
        return db.session.query(exists().where(getattr(table, attribute) == value)).scalar()
    else:
        return (db.session.query(table).where(getattr(table, attribute) == value).first()).as_dict()

def get_interval(type):
    valid_types = automatic_intervals.keys()
    if type not in valid_types:
        raise ValueError(write_value_error(type, valid_types))
    return int(automatic_intervals[type]) / db.session.query(func.count(Token.user_id)).scalar()

def get_score_out(attribute, value, check_presence_only=None):
    return get_object_out(Score, attribute, value, check_presence_only)
    
def get_token_out(attribute, value, check_presence_only=None):
    return get_object_out(Token, attribute, value, check_presence_only)
    
def get_user_out(attribute, value, check_presence_only=None):
    return get_object_out(User, attribute, value, check_presence_only)

def get_user_score_endpoint(user_id):
    return f'/users/{user_id}/scores/recent'

def refresh_token(refresh_token):
    response = requests.post(
        endpoints['BASE_URL'] + endpoints['TOKEN'],
        headers=get_headers(),
        data=get_refresh_payload(refresh_token)
    )
    return response.json()

def select_all(table, sort_by, attribute=None, value=None):
    valid_attributes = table.__table__.columns.keys()
    if sort_by not in valid_attributes:
        raise ValueError(write_value_error(table, valid_attributes))
    data = {}
    query = db.session.query(table)
    if attribute:
        query = query.where(getattr(table, attribute) == value)
    all_obj = db.session.query(table).order_by(getattr(table, sort_by).desc()).all()
    for obj in all_obj:
        data.update(obj.as_dict())
    return data
    
def store_recent_scores(user_id):
    token_data = get_token_out('user_id', user_id, False)
    response = requests.get(
        endpoints['BASE_URL'] + endpoints['V2'] + get_user_score_endpoint(user_id),
        headers=get_headers(token_data['access_token']),
        data=score_parameters,
    )
    scores = response.json()
    for score in scores:
        score_id = _.get(score, score_attributes['id'])
        if not get_score_out('id', score_id, True):
            db.session.add(
                Score(
                    id=score_id,
                    user_id=user_id,
                    timestamp=dateutil.parser.isoparse(_.get(score, score_attributes['timestamp'])),
                    notes=(
                        _.get(score, score_attributes['count_300']) +
                        _.get(score, score_attributes['count_100']) +
                        _.get(score, score_attributes['count_50'])
                    ),
                    accuracy=_.get(score, score_attributes['accuracy']),                    
                )
            )
    db.session.commit()

def write_value_error(invalid, valid):
    valid_types = ', '.join(valid)
    return f'invalid type \'{invalid}. valid types: {valid_types}.'
