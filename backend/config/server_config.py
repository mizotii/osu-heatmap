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

daily_statistics = {
    'play_count': UserDailyStatistics.play_count,
    'play_time': UserDailyStatistics.play_time,
    'ranked_score': UserDailyStatistics.ranked_score,
    'total_hits': UserDailyStatistics.total_hits,
    'total_score': UserDailyStatistics.total_score,
}

database = {
    'db_uri': os.environ.get('DB_URI'),
}

endpoints = {
    # auth
    'oauth': 'https://osu.ppy.sh/oauth/authorize',
    'callback': 'https://mizotii-api.xyz/callback',

    # callback
    'token': 'https://osu.ppy.sh/oauth/token',

    # osu api main
    'v2': 'https://osu.ppy.sh/api/v2',

    # osu api endpoints
    'self': '/me',

    # rulesets
    'osu': '/me/osu',
    'taiko': '/me/taiko',
    'fruits': '/me/fruits',
    'mania': '/me/mania',

    # client
    'frontend': 'https://osu-heatm.app',
}

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
}

rulesets = [
    'osu', 'taiko', 'fruits', 'mania',
]

ruleset_tables = {
    'osu': UserOsu,
    'taiko': UserTaiko,
    'fruits': UserCatch,
    'mania': UserMania,
}