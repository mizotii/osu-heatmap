import os

attributes = {
    'id': 'id',
    'name': 'username',
    'global_rank': 'statistics.global_rank',
}

automatic_intervals = {
    'REFRESH_TOKEN': '43200',
    'REFRESH_PROFILE': '7200',
}

client_credentials = {
    'CLIENT_ID': os.environ.get('CLIENT_ID'),
    'CLIENT_SECRET': os.environ.get('CLIENT_SECRET'),
}

constraints = {
    'MAX_TOKEN_LENGTH': 2000,
    'MAX_TYPE_LENGTH': 6,
    'MAX_USER_LENGTH': 15,
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

def get_token_payload(code):
    payload = {
        'client_id': client_credentials['CLIENT_ID'],
        'client_secret': client_credentials['CLIENT_SECRET'],
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': endpoints['REDIRECT_URI'],
    }
    return payload

def get_user_score_endpoint(id):
    return f'/users/{id}/scores/recent'