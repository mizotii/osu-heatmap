import os
class Config:
    CLIENT_ID = os.environ.get['CLIENT_ID']
    CLIENT_SECRET = os.environ.get['CLIENT_SECRET']

class Endpoints:
    AUTHORIZATION_URL = 'https://osu.ppy.sh/oauth/authorize'
    REDIRECT_URI = 'http://localhost:5000/callback'
