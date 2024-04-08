import os

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
    'BASE_URL': 'https://osu.ppy.sh/',
    'REDIRECT_URI': 'http://localhost:5000/callback',
    'AUTHORIZATION': 'oauth/authorize',
    'TOKEN': 'oauth/token',
    'THIS_USER': '/api/v2/me/',
}

def get_headers(token=None):
    headers =  {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    if token:
        headers['Authorization'] = f'Bearer {token}'
    return headers