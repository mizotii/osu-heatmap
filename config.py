import os

data = {
    'client_credentials': {
        'CLIENT_ID': os.environ.get('CLIENT_ID'),
        'CLIENT_SECRET': os.environ.get('CLIENT_SECRET'),
    },
    'endpoints': {
        'AUTHORIZATION_URL': 'https://osu.ppy.sh/oauth/authorize',
        'TOKEN_URL': 'https://osu.ppy.sh/oauth/token',
        'REDIRECT_URI': 'http://localhost:5000/callback',
    },
}
