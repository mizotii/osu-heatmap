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

profile_data = {
    'USERNAME': 'null',
    'GLOBAL_RANK': 'null',
    'SCORES': {},
}

score_parameters = {
    'scope': 'public',
    'include_fails': '1',
    'mode': 'osu',
}

user_search = {
    'USER_FOUND': False,
    'USER_ID': 'null',
}

def get_headers(base, token=None):
    headers =  {
        'Accept': 'application/json',
    }
    if base:
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
    else:
        headers['Content-Type'] = 'application/json'
    if token:
        headers['Authorization'] = f'Bearer {token}'
    return headers

def get_user_score_endpoint(id):
    return f'/users/{id}/scores/recent'