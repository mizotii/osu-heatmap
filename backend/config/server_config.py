import dateutil.parser
import os
import pydash as _
import requests
from datetime import datetime, timedelta
from models import db, Beatmap, BeatmapSet, Score, Token, User, UserCatch, UserDailyStatistics, UserMania, UserOsu, UserTaiko
from sqlalchemy import and_, between, exists
from urllib.parse import urlencode, urljoin

beatmap_attributes = {
    'beatmapset_id': 'beatmapset_id',
    'difficulty_rating': 'difficulty_rating',
    'id': 'id',
    'ruleset': 'mode',
    'total_length': 'hit_length',
    'version': 'version',
}

beatmapset_attributes = {
    'artist': 'artist',
    'artist_unicode': 'artist_unicode',
    'id': 'id',
    'creator': 'creator',
    'creator_id': 'user_id',
    'slimcover': 'covers.slimcover',
    'slimcover_2x': 'covers.slimcover@2x',
    'status': 'status',
    'title': 'title',
    'title_unicode': 'title_unicode',
}

client_credentials = {
    'client_id': os.environ['CLIENT_ID'],
    'client_secret': os.environ['CLIENT_SECRET'],
}

database = {
    'db_uri': os.environ['DB_URI'],
}

endpoints = {
    'authorize': 'https://osu.ppy.sh/oauth/authorize',
    'api': 'https://osu.ppy.sh/api/v2',
    'callback': 'http://localhost:5000/callback',
    'this_user': {
        'osu': '/me',
        'taiko': '/me/taiko',
        'fruits': '/me/fruits',
        'mania': '/me/mania',
    },
    'token': 'https://osu.ppy.sh/oauth/token',
}

intervals = {
    'dailies': {
        'hour': 0,
        'interval': 1,
    },
    'hours': 24,
    'hours_to_seconds': 3600.0,
    'refresh': {
        'interval': '*/2',
    },
    'users': {
        'interval': '*/8',
    }
}

rulesets = [
    'fruits', 'mania', 'osu', 'taiko', 
]

score_attributes = {
    'id': 'current_user_attributes.pin.score_id',
    'user_id': 'user_id',
    'timestamp': 'created_at',
    'ruleset': 'mode',
    'count_300': 'statistics.count_300',
    'count_100': 'statistics.count_100',
    'count_50': 'statistics.count_50',
    'count_geki': 'statistics.count_geki',
    'count_katu': 'statistics.count_katu',
    'count_miss': 'statistics.count_miss',
    'accuracy': 'accuracy',
    'beatmap_id': 'beatmap.id',
    'beatmapset_id': 'beatmap.beatmapset_id',
    'max_combo': 'max_combo',
    'mods': 'mods',
    'passed': 'passed',
    'rank': 'rank',
    'score': 'score',
}

tables = {
    'fruits': UserCatch,
    'mania': UserMania,
    'osu': UserOsu,
    'taiko': UserTaiko,
}

token_attributes = {
    'access_token': 'access_token',
    'expires_at': 'expires_in',
    'refresh_token': 'refresh_token',
    'token_type': 'token_type',
}

user_attributes = {
    'avatar_url': 'avatar_url',
    'country_code': 'country_code',
    'cover_url': 'cover.url',
    'id': 'id',
    'is_deleted': 'is_deleted',
    'is_restricted': 'is_restricted',
    'playmode': 'playmode',
    'play_count': 'statistics.play_count',
    'play_time': 'statistics.play_time',
    'ranked_score': 'statistics.ranked_score',
    'total_hits': 'statistics.total_hits',
    'total_score': 'statistics.total_score',
    'username': 'username',
}

# requires above config

authorization_parameters = {
    'client_id': client_credentials['client_id'],
    'redirect_uri': endpoints['callback'],
    'response_type': 'code',
    'scope': 'public identify',
    'state': 'randomval',
}

def create_authorization_url():
    return urljoin(endpoints['authorize'], '?' + urlencode(authorization_parameters))

def calculate_expiration(interval):
    return (datetime.now() + timedelta(seconds=interval))

def create_headers(token=None):
    headers = {
        'Accept': 'application/json',
    }
    if token:
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = f'Bearer {token}'
    else:
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
    return headers

# todo: add scores, beatmaps, beatmapsets
def create_profile(id, ruleset):
    if ruleset not in rulesets:
        raise ValueError(write_value_error(ruleset, rulesets))
    user = get_object(User, 'id', id, as_dict=True)
    user_ruleset = get_object(tables[ruleset], 'id', id, as_dict=True)
    rows = db.session.query(UserDailyStatistics).\
        filter(
            and_(
                UserDailyStatistics.id == id,
                UserDailyStatistics.ruleset == ruleset,
            )
        ).all()
    data = []
    if rows:
        for day in rows:
            data.append(day.as_dict())
    profile = {
        'user': user,
        'user_ruleset': user_ruleset,
        'user_heatmap_data': data,
    }
    return profile

def create_refresh_parameters(refresh):
    if not refresh:
        raise ValueError('could not create refresh token parameters: no refresh token provided')
    params = {
        'client_id': client_credentials['client_id'],
        'client_secret': client_credentials['client_secret'],
        'grant_type': 'refresh_token',
        'refresh_token': refresh,
        'scope': 'public identify',
    }
    return params

def create_recents_endpoint(id):
    return f'/users/{id}/scores/recent'

def create_recents_parameters(ruleset):
    if ruleset not in rulesets:
        raise ValueError(write_value_error(ruleset, rulesets))
    params = {
        'include_fails': '1',
        'limit': 999,
        'mode': ruleset,
    }
    return params

def create_score_list(id, ruleset, timestamp):
    start = datetime.fromtimestamp(timestamp / 1000)
    data_banners = db.session.query(Score, Beatmap, BeatmapSet).\
        where(
            and_(
                Score.user_id == id,
                Score.ruleset == ruleset,
                between(Score.timestamp, start, start + timedelta(days=1)),
            )
        ).\
        where(Score.beatmap_id == Beatmap.id).\
        where(Beatmap.beatmapset_id == BeatmapSet.id).\
        all()
    scores = []
    if data_banners:
        for score, beatmap, beatmapset in data_banners:
            scores.append({
                'score_data': score.as_dict(),
                'beatmap_data': beatmap.as_dict(),
                'beatmapset_data': beatmapset.as_dict(),
            })
    return scores

def create_token_parameters(code):
    if not code:
        raise ValueError('could not create token parameters: no code provided')
    params = {
        'client_id': client_credentials['client_id'],
        'client_secret': client_credentials['client_secret'],
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': endpoints['callback'],
    }
    return params

def delete_expired_tokens():
    tokens = select_all(Token, sort_by=Token.expires_at)
    now = datetime.now()
    for token in tokens:
        if (getattr(token, 'expires_at') < now):
            db.session.delete(token)
    db.session.commit()

# updates general user and osu ruleset for user by default (osu)
def direct_update_user(id, token, ruleset):
    if ruleset == 'osu':
        table = User
        old_user = get_object(table, 'id', id)
        new_user = fetch_user(token['access_token'])
        update_user(table, old_user, new_user)
    table = tables[ruleset]
    old_user = get_object(table, 'id', id)
    new_user = fetch_user(token['access_token'], ruleset)
    update_user(table, old_user, new_user)

def fetch_recent_scores(id, ruleset):
    token = get_object(Token, 'user_id', id)
    response = requests.get(
        endpoints['api'] + urljoin(create_recents_endpoint(id), '?' + urlencode(create_recents_parameters(ruleset))),
        headers=create_headers(getattr(token, 'access_token'))
    )
    return response.json()

def fetch_token(code):
    response = requests.post(
        endpoints['token'],
        headers=create_headers(),
        data=create_token_parameters(code)
    )
    return response.json()

def fetch_user(access, ruleset='osu', attribute=None):
    if ruleset not in rulesets:
        raise ValueError(write_value_error(ruleset, rulesets))
    response = requests.get(
        endpoints['api'] + endpoints['this_user'][ruleset],
        headers=create_headers(access)
    )
    data = response.json()
    if attribute:
        if attribute not in user_attributes:
            raise ValueError(write_value_error(attribute, user_attributes))
        return _.get(data, user_attributes[attribute])
    return data

def get_object(table, attribute, value, check_exists_only=False, as_dict=False):
    valid_attributes = table.__table__.columns.keys()
    if attribute not in valid_attributes:
        raise ValueError(write_value_error(attribute, valid_attributes))
    if check_exists_only:
        return db.session.query(exists().where(getattr(table, attribute) == value)).scalar()
    else:
        query = (db.session.query(table).where(getattr(table, attribute) == value).first())
        if not as_dict:
            return query
        else:
            return query.as_dict()

def handle_authorization(token):
    id = fetch_user(token['access_token'], attribute='id')
    hyp_user = get_object(Token, 'user_id', id)

    # schema draws Token as parent class, meaning if a Token exists, so does its User in all facets
    if hyp_user:
        handle_token(hyp_user, token)
        for ruleset in rulesets:
            update_user_scores(id, ruleset)
            direct_update_user(id, token, ruleset)
    else:
        store_token(id, token)
        store_user(token)
        for ruleset in rulesets:
            update_user_scores(id, ruleset)
            store_user_ruleset(token, ruleset)

def handle_token(user, token):
    for key in Token.__table__.columns.keys():
        if key not in ('user_id', 'expires_at'):
            setattr(user, key, _.get(token, token_attributes[key]))
    setattr(user, 'expires_at', calculate_expiration(token['expires_in']))
    db.session.commit()
    
def refresh_token(token):
    response = requests.get(
        endpoints['token'],
        headers=create_headers(),
        data=create_refresh_parameters(token['refresh'])
    )
    handle_token(response.json())

def select_all(table, attribute=None, attribute_value=None, join_by_column_other=None, join_by_column_this=None, join_by_table=None, sort_by=None, as_dict=False):
    data = []
    query = db.session.query(table)
    if attribute:
        query = query.where(getattr(table, attribute) == attribute_value)
    if join_by_column_other and join_by_column_this and join_by_table:
        query = query.join(join_by_table, join_by_column_other == join_by_column_this)
    if sort_by:
        query = query.order_by(sort_by.desc())
    all_obj = query.all()
    for obj in all_obj:
        data.append(obj.as_dict()) if as_dict else data.append(obj)
    return data

def store_beatmap(beatmap):
    db.session.add(
        Beatmap(
            beatmapset_id=_.get(beatmap, beatmap_attributes['beatmapset_id']),
            difficulty_rating=_.get(beatmap, beatmap_attributes['difficulty_rating']),
            id=_.get(beatmap, beatmap_attributes['id']),
            ruleset=_.get(beatmap, beatmap_attributes['ruleset']),
            total_length=_.get(beatmap, beatmap_attributes['total_length']),
            version=_.get(beatmap, beatmap_attributes['version']),
        )
    )
    db.session.commit()

def store_beatmapset(beatmapset):
    db.session.add(
        BeatmapSet(
            artist=_.get(beatmapset, beatmapset_attributes['artist']),
            artist_unicode=_.get(beatmapset, beatmapset_attributes['artist_unicode']),
            id=_.get(beatmapset, beatmapset_attributes['id']),
            slimcover=_.get(beatmapset, beatmapset_attributes['slimcover']),
            slimcover_2x=_.get(beatmapset, beatmapset_attributes['slimcover_2x']),
            creator=_.get(beatmapset, beatmapset_attributes['creator']),
            creator_id=_.get(beatmapset, beatmapset_attributes['creator_id']),
            status=_.get(beatmapset, beatmapset_attributes['status']),
            title=_.get(beatmapset, beatmapset_attributes['title']),
            title_unicode=_.get(beatmapset, beatmapset_attributes['title_unicode']),
        )
    )
    db.session.commit()

def store_daily_statistics(id, ruleset, date, play_time, play_count, note_count, ranked_score, total_score):
    db.session.add(
        UserDailyStatistics(
            id=id,
            ruleset=ruleset,
            start_date=date,
            play_time=play_time,
            play_count=play_count,
            note_count=note_count,
            ranked_score=ranked_score,
            total_score=total_score,
        )
    )

    # streak counter
    if all(stat > 0 for stat in (play_time, play_count, note_count, ranked_score, total_score)):
        user = get_object(tables[ruleset], 'id', id)
        current_streak = getattr(user, 'streak_current')
        longest_streak = getattr(user, 'streak_longest')
        setattr(user, 'streak_current', current_streak + 1)
        if current_streak > longest_streak:
            setattr(user, 'streak_longest', current_streak)
    db.session.commit()

def store_score(score):
    db.session.add(
        Score(
            id=_.get(score, score_attributes['id']),
            user_id=_.get(score, score_attributes['user_id']),
            timestamp=dateutil.parser.isoparse(_.get(score, score_attributes['timestamp'])),
            ruleset=_.get(score, score_attributes['ruleset']),
            count_300=_.get(score, score_attributes['count_300']),
            count_100=_.get(score, score_attributes['count_100']),
            count_50=_.get(score, score_attributes['count_50']),
            count_geki=_.get(score, score_attributes['count_geki']),
            count_katu=_.get(score, score_attributes['count_katu']),
            count_miss=_.get(score, score_attributes['count_miss']),
            notes=total_notes(score),
            accuracy=round(_.get(score, score_attributes['accuracy']), 4) * 100,
            beatmap_id=_.get(score, score_attributes['beatmap_id']),
            beatmapset_id=_.get(score, score_attributes['beatmapset_id']),
            max_combo=_.get(score, score_attributes['max_combo']),
            mods=' '.join(_.get(score, score_attributes['mods'])),
            passed=_.get(score, score_attributes['passed']),
            rank=_.get(score, score_attributes['rank']),
            score=_.get(score, score_attributes['score']),
        )
    )
    db.session.commit()

# stores token, then stores all four user rulesets
def store_token(id, token):
    db.session.add(
        Token(
            user_id=id,
            access_token=token['access_token'],
            expires_at=(calculate_expiration(token['expires_in'])),
            refresh_token=token['refresh_token'],
            token_type=token['token_type'],
        )
    )
    db.session.commit()

# todo: rework a la update functions
def store_user(token):
    user = fetch_user(token['access_token'])
    db.session.add(
        User(
            avatar_url=_.get(user, user_attributes['avatar_url']),
            country_code=_.get(user, user_attributes['country_code']),
            cover_url=_.get(user, user_attributes['cover_url']),
            id=_.get(user, user_attributes['id']),
            is_deleted=_.get(user, user_attributes['is_deleted']),
            is_restricted=_.get(user, user_attributes['is_restricted']),
            last_updated=datetime.now(),
            playmode=_.get(user, user_attributes['playmode']),
            registration_date=datetime.now(),
            username=_.get(user, user_attributes['username']),
        )
    )
    db.session.commit()

def store_user_ruleset(token, ruleset):
    user_ruleset = fetch_user(token['access_token'], ruleset)
    db.session.add(
        tables[ruleset](
            id=_.get(user_ruleset, user_attributes['id']),
            last_updated=datetime.now(),
            username=_.get(user_ruleset, user_attributes['username']),
            play_count=_.get(user_ruleset, user_attributes['play_count']),
            play_time=_.get(user_ruleset, user_attributes['play_time']),
            ranked_score=_.get(user_ruleset, user_attributes['ranked_score']),
            streak_current=0,
            streak_longest=0,
            total_hits=_.get(user_ruleset, user_attributes['total_hits']),
            total_score=_.get(user_ruleset, user_attributes['total_score']),
        )
    )
    db.session.commit()

def total_notes(score):
    return sum((score['statistics'][key] or 0) for key in score['statistics'] if key != 'count_miss')

def update_user(table, old_user, new_user):
    for key in table.__table__.columns.keys():
        if key not in ('id', 'last_updated', 'streak_current', 'streak_longest', 'registration_date'):
            setattr(old_user, key, _.get(new_user, user_attributes[key]))
    setattr(old_user, 'last_updated', datetime.now())
    db.session.commit()

def update_user_scores(id, ruleset):
    scores = fetch_recent_scores(id, ruleset)
    for score in scores:
        beatmap = score['beatmap']
        beatmapset = score['beatmapset']
        if not get_object(BeatmapSet, 'id', _.get(beatmapset, beatmapset_attributes['id']), check_exists_only=True):
            store_beatmapset(beatmapset)
        if not get_object(Beatmap, 'id', _.get(beatmap, beatmap_attributes['id']), check_exists_only=True):
            store_beatmap(beatmap)
        if not get_object(Score, 'id', _.get(score, score_attributes['id']), check_exists_only=True):
            store_score(score)

def write_value_error(invalid, valid):
    valid_types = ', '.join(valid)
    return f'invalid type \'{invalid}. valid types: {valid_types}.'
