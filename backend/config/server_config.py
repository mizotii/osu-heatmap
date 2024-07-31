import dateutil.parser
import os
import pydash as _
import requests
from datetime import datetime, timedelta
from models import db, Beatmap, BeatmapSet, Score, Token, User, UserCatch, UserDailyStatistics, UserMania, UserOsu, UserTaiko
from sqlalchemy import and_, between, desc, exists
from urllib.parse import urlencode, urljoin

credentials = {
    'client_id': os.environ.get('CLIENT_ID'),
    'client_secret': os.environ.get('CLIENT_SECRET'),
}