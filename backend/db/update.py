"""for writing to the database"""

from datetime import date, datetime, timedelta
from db.models import db, User, UserOsu, UserTaiko, UserCatch, UserMania, UserDailyStatistics, Score, Beatmap, BeatmapSet, ClientCredentialsKey
from config.osu_api import fetch as ft
from config import server_config as sc
from sqlalchemy import delete
import dateutil.parser
import db.read as rd
import requests

user_ruleset_attributes = [
    'last_updated',
    'username',
]

def refresh_client_credentials():
    key = ClientCredentialsKey.query.first()
    if key:
        db.session.execute(delete(ClientCredentialsKey))
    url = sc.endpoints['token']
    payload = {
        'client_id': sc.credentials['client_id'],
        'client_secret': sc.credentials['client_secret'],
        'grant_type': 'client_credentials',
        'scope': 'public',
    }
    r = requests.post(url=url, headers=sc.headers, data=payload).json()
    store_client_key(r)

def store_user(token, user):
    db.session.add(User(
        id=user['id'],
        access_token=token['access_token'],
        token_type=token['token_type'],

        avatar_url=user['avatar_url'],
        country_code=user['country_code'],
        cover_url=user['cover']['url'],
        is_deleted=user['is_deleted'],
        last_updated=datetime.now(),
        playmode=user['playmode'],
        registration_date=datetime.now(),
        username=user['username'],

        streak_current=0,
        streak_longest=0,
    ))
    db.session.commit()

def store_user_ruleset(data, ruleset, id):
    db.session.add(sc.ruleset_tables[ruleset](
        accumulated_play_count=0,
        accumulated_play_time=0,
        accumulated_total_hits=0,
        accumulated_ranked_score=0,
        accumulated_total_score=0,
        id=id,
        last_updated=datetime.now(),
        username=data['username'],
        play_count=data['statistics']['play_count'],
        play_time=data['statistics']['play_time'],
        ranked_score=data['statistics']['ranked_score'],
        streak_current=0,
        streak_longest=0,
        total_hits=data['statistics']['total_hits'],
        total_score=data['statistics']['total_score'],
    ))
    db.session.commit()

def store_user_daily(ruleset, id):
    db.session.add(UserDailyStatistics(
        id=id,
        ruleset=ruleset,
        start_date=date.today(),
        play_time=0,
        play_count=0,
        total_hits=0,
        ranked_score=0,
        streak_counted=False,
        total_score=0,
    ))
    db.session.commit()

def store_scores(app, id, ruleset):
    with app.app_context():
        scores = ft.fetch_scores(id, ruleset)
        for score in scores:
            beatmap = score['beatmap']
            beatmapset = score['beatmapset']
            map = rd.read_beatmap(beatmap['id'], beatmapset['id'])
            set = rd.read_beatmapset(beatmapset['id'])
            potential_score = rd.read_score(score['user_id'], score['created_at'])
            if not set:
                store_beatmapset(beatmapset)
            if not map:
                store_beatmap(beatmap)
            if not potential_score:
                store_score(score)

def store_beatmap(beatmap):
    db.session.add(Beatmap(
        beatmapset_id=beatmap['beatmapset_id'],
        difficulty_rating=beatmap['difficulty_rating'],
        id=beatmap['id'],
        ruleset=beatmap['mode'],
        total_length=beatmap['hit_length'],
        version=beatmap['version'],
    ))
    db.session.commit()

def store_beatmapset(beatmapset):
    db.session.add(BeatmapSet(
        artist=beatmapset['artist'],
        artist_unicode=beatmapset['artist_unicode'],
        id=beatmapset['id'],
        creator=beatmapset['creator'],
        creator_id=beatmapset['user_id'],
        slimcover=beatmapset['covers']['slimcover'],
        slimcover_2x=beatmapset['covers']['slimcover@2x'],
        status=beatmapset['status'],
        title=beatmapset['title'],
        title_unicode=beatmapset['title_unicode'],
    ))
    db.session.commit()

def store_score(score):
    db.session.add(Score(
        user_id=score['user_id'],
        timestamp=dateutil.parser.isoparse(score['created_at']),
        ruleset=score['mode'],
        count_300=score['statistics']['count_300'],
        count_100=score['statistics']['count_100'],
        count_50=score['statistics']['count_50'],
        count_geki=score['statistics']['count_geki'],
        count_katu=score['statistics']['count_katu'],
        count_miss=score['statistics']['count_miss'],
        notes=total_notes(score),
        accuracy=round(score['accuracy'], 4) * 100.00,
        beatmap_id=score['beatmap']['id'],
        beatmapset_id=score['beatmap']['beatmapset_id'],
        max_combo=score['max_combo'],
        mods=' '.join(score['mods']),
        passed=score['passed'],
        rank=score['rank'],
        score=score['score'],
    ))
    db.session.commit()

def store_client_key(token):
    db.session.add(ClientCredentialsKey(
        access_token=token['access_token'],
        expires_at=timedelta(seconds=token['expires_in'])+datetime.now(),
        token_type=token['token_type'],
    ))
    db.session.commit()

def total_notes(score):
    return sum((score['statistics'][key] or 0) for key in score['statistics'] if key != 'count_miss')

def update_user_statistics(app, user):
    with app.app_context():
        id = user.__dict__['id']

        update_user(app, id)

        for ruleset in sc.rulesets:
            updated_statistics = ft.fetch_user(id, ruleset)
            old_ruleset = rd.read_ruleset(id, ruleset)
            store_scores(app, id, ruleset)

            if not old_ruleset:
                store_user_ruleset(updated_statistics, ruleset, id)
                store_user_daily(ruleset, id)
            else:

                # heatmap cell

                old_cell = rd.read_cell(id, ruleset, date.today())
                if not old_cell:
                    store_user_daily(ruleset, id)
                else:
                    play_time_diff = (updated_statistics['statistics']['play_time'] - old_ruleset.__dict__['play_time'])

                    # ruleset: streaks

                    # first check whether streak should be reset
                    yesterday_cell = rd.read_cell(id, ruleset, date.today() - timedelta(days=1))
                    if yesterday_cell.streak_counted is False:
                        setattr(old_ruleset, 'streak_current', 0)
                        db.session.commit()
                        db.session.refresh(old_cell)

                    # then check for streak
                    if old_cell.streak_counted is False and play_time_diff > 0:
                        setattr(old_ruleset, 'streak_current', getattr(old_ruleset, 'streak_current') + 1)

                        # update longest streak if necessary
                        if getattr(old_ruleset, 'streak_current') > getattr(old_ruleset, 'streak_longest'):
                            setattr(old_ruleset, 'streak_longest', getattr(old_ruleset, 'streak_current'))

                    # update all other attributes
                    play_count_diff = updated_statistics['statistics']['play_count'] - old_ruleset.__dict__['play_count']
                    total_hits_diff = updated_statistics['statistics']['total_hits'] - old_ruleset.__dict__['total_hits']
                    ranked_score_diff = updated_statistics['statistics']['ranked_score'] - old_ruleset.__dict__['ranked_score']
                    total_score_diff = updated_statistics['statistics']['total_score'] - old_ruleset.__dict__['total_score']

                    setattr(old_cell, 'play_time', play_time_diff + getattr(old_cell, 'play_time'))                    
                    setattr(old_cell, 'play_count', play_count_diff + getattr(old_cell, 'play_count'))                    
                    setattr(old_cell, 'total_hits', total_hits_diff + getattr(old_cell, 'total_hits'))                    
                    setattr(old_cell, 'ranked_score', ranked_score_diff + getattr(old_cell, 'ranked_score'))                
                    setattr(old_cell, 'total_score', total_score_diff + getattr(old_cell, 'total_score'))
                    db.session.commit()
                    db.session.refresh(old_cell)
                    
                # todo: update ruleset attributes for everything except streaks using collection above
                
                # ruleset
                setattr(old_ruleset, 'accumulated_play_count', getattr(old_ruleset, 'play_count') + play_count_diff)
                setattr(old_ruleset, 'accumulated_play_time', getattr(old_ruleset, 'play_time') + play_time_diff)
                setattr(old_ruleset, 'accumulated_ranked_score', getattr(old_ruleset, 'ranked_score') + ranked_score_diff)
                setattr(old_ruleset, 'accumulated_total_hits', getattr(old_ruleset, 'total_hits') + total_hits_diff)
                setattr(old_ruleset, 'accumulated_total_score', getattr(old_ruleset, 'total_score') + total_score_diff)
                
                setattr(old_ruleset, 'last_updated', datetime.now())
                setattr(old_ruleset, 'username', updated_statistics['username'])
                setattr(old_ruleset, 'play_count', updated_statistics['statistics']['play_count'])
                setattr(old_ruleset, 'play_time', updated_statistics['statistics']['play_time'])
                setattr(old_ruleset, 'ranked_score', updated_statistics['statistics']['ranked_score'])
                setattr(old_ruleset, 'total_hits', updated_statistics['statistics']['total_hits'])
                setattr(old_ruleset, 'total_score', updated_statistics['statistics']['total_score'])
                db.session.commit()
                db.session.refresh(old_ruleset)

def update_user(app, id):
    with app.app_context():
        old_user = rd.read_user(id)
        new_user = ft.fetch_user(id)
        setattr(old_user, 'avatar_url', new_user['avatar_url'])
        setattr(old_user, 'country_code', new_user['country_code'])
        setattr(old_user, 'cover_url', new_user['cover']['url'])
        setattr(old_user, 'is_deleted', new_user['is_deleted'])
        setattr(old_user, 'last_updated', datetime.now())
        setattr(old_user, 'playmode', new_user['playmode'])
        db.session.commit()
        db.session.refresh(old_user)

def update_user_token(token, user):
    setattr(user, 'access_token', token['access_token'])
    setattr(user, 'token_type', token['token_type'])
    db.session.commit()
    db.session.refresh(user)