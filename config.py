import os

data = {
    'client_credentials': {
        'CLIENT_ID': os.environ.get('OH_CLIENT_ID'),
        'CLIENT_SECRET': os.environ.get('OH_CLIENT_SECRET'),
    },
    'endpoints': {
        'AUTHORIZATION_URL': 'https://osu.ppy.sh/oauth/authorize',
        'REDIRECT_URI': 'http://localhost:5000/callback',
    },
}
