import os
import pydash as _
import requests
from models import db, Class, Score, Token, User
from sqlalchemy import exists
from urllib.parse import urlencode, urljoin

automatic_intervals = {
    'REFRESH_TOKEN': '43200',
    'REFRESH_PROFILE': '7200',
}

client_credentials = {
    'CLIENT_ID': os.environ.get('CLIENT_ID'),
    'CLIENT_SECRET': os.environ.get('CLIENT_SECRET'),
}

database = {
    'DB_URI': os.environ.get('DB_URI'),
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

score_parameters = {
    'scope': 'public',
    'include_fails': '1',
    'mode': 'osu',
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

def get_user_in(operation_type, token_data):
    valid_operations = ['refresh', 'update']
    if operation_type not in valid_operations:
        raise ValueError(write_value_error(operation_type, valid_operations))
    
    access = token_data.get('access_token')
    refresh = token_data.get('refresh_token')

    # creates a new user if they aren't found, updates an old user if they are
    if operation_type == 'update':
        response = requests.get(
            endpoints['BASE_URL'] + endpoints['V2'] + endpoints['THIS_USER'],
            headers=get_headers(access)
        )
        new_user_data = response.json()
        new_user_id = new_user_data.get('id')

        # if user exists
        if get_object_out(User, 'id', new_user_id, True) and get_object_out(Token, 'user_id', new_user_id, True):
            old_user_data = get_object_out(User, 'id', new_user_id, False)
            for key in User.__table__.columns.keys():
                if key != 'id':
                    old_user_data[key] = _.get(new_user_data, user_attributes[key])
            

        # if user is new
        else:
            db.session.add(
                User(
                    id=new_user_id,
                    name=new_user_data.get(user_attributes['name']),
                    global_rank=_.get(new_user_data, user_attributes['global_rank']),
                ),
                Token(
                    user_id=new_user_id,
                    access_token=access,
                    expires_in=token_data.get('expires_in'),
                    refresh_token=refresh,
                    token_type=token_data.get('token_type'),
                )
            )

    # refreshes token
    else:
        old_token = get_object_out(Token, 'access_token', access, False)
        new_token = refresh_token(refresh)
        for key in Token.__table__.columns.keys():
            if key != 'user_id':
                setattr(old_token, key, _.get(new_token, key))


    # applies to either operation
    db.session.commit()

# functions as a user presence checker if last arg is True
def get_object_out(table, attribute_type, value, check_presence_only=None):
    valid_attributes = table.__table__.columns.keys()
    if attribute_type not in valid_attributes:
        raise ValueError(write_value_error(attribute_type, valid_attributes))
    if check_presence_only:
        return db.session.query(exists().where(getattr(table, attribute_type) == value)).scalar()
    else:
        return (db.session.query(table).where(getattr(table, attribute_type) == value).first()).as_dict()
    
def get_token_out(attribute_type, value, check_presence_only=None):
    return get_object_out(Token, attribute_type, value, check_presence_only)
    
def get_user_out(attribute_type, value, check_presence_only=None):
    return get_object_out(User, attribute_type, value, check_presence_only)

def get_user_score_endpoint(user_id):
    return f'/users/{user_id}/scores/recent'

def refresh_token(refresh_token):
    response = requests.post(
        endpoints['BASE_URL'] + endpoints['TOKEN'],
        headers=get_headers(True),
        data=get_refresh_payload(refresh_token)
    )
    return response.json()

def write_value_error(invalid, valid):
    valid_types = ', '.join(valid)
    return f'invalid type \'{invalid}. valid types: {valid_types}.'
