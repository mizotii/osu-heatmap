import os

class Config:
    DEBUG = False
    CLIENT_ID = os.environ.get("OH_CLIENT_ID")
    CLIENT_SECRET = os.environ.get("OH_CLIENT_SECRET")
    REDIRECT_URI = "http://localhost:5000/callback"
    AUTH_URL = f"https://osu.ppy.sh/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=public+identify&state=randomval"
    TOKEN_URL = "https://osu.ppy.sh/oauth/token"
    OH_DB_URI = os.environ.get("OH_DB_URI")