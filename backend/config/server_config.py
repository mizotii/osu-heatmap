import dateutil.parser
import os
import pydash as _
import requests
from datetime import datetime, timedelta
from db.models import db, Beatmap, BeatmapSet, Score, User, UserCatch, UserDailyStatistics, UserMania, UserOsu, UserTaiko
from sqlalchemy import and_, between, desc, exists
from urllib.parse import urlencode, urljoin

credentials = {
    'client_id': os.environ.get('CLIENT_ID'),
    'client_secret': os.environ.get('CLIENT_SECRET'),
    'sessions_key': os.environ.get('SESSIONS_SECRET'),
}

database = {
    'db_uri': os.environ.get('DB_URI'),
}

endpoints = {
    # auth
    'oauth': 'https://osu.ppy.sh/oauth/authorize',
    'callback': 'http://localhost:5000/callback',

    # callback
    'token': 'https://osu.ppy.sh/oauth/token',

    # osu api main
    'v2': 'https://osu.ppy.sh/api/v2',

    # osu api endpoints
    'user': '/me',

    # rulesets
    'osu': '/me/osu',
    'taiko': '/me/taiko',
    'fruits': '/me/fruits',
    'mania': '/me/mania',
}

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
}

ruleset_tables = {
    'osu': UserOsu,
    'taiko': UserTaiko,
    'fruits': UserCatch,
    'mania': UserMania,
}