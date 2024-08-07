"""for writing to the database"""

from datetime import date, datetime, timedelta
from db.models import db, User, UserOsu, UserTaiko, UserCatch, UserMania, UserDailyStatistics, Score, Beatmap, BeatmapSet
from config.osu_api import fetch as ft
from config import server_config as sc
import db.read as rd

user_ruleset_attributes = [
    'last_updated',
    'username',
]

def store_user(token, user):
    db.session.add(User(
        id=user['id'],
        access_token=token['access_token'],
        expires_at=timedelta(seconds=token['expires_in'])+datetime.now(),
        refresh_token=token['refresh_token'],
        token_type=token['token_type'],

        avatar_url=user['avatar_url'],
        country_code=user['country_code'],
        cover_url=user['cover']['url'],
        is_deleted=user['is_deleted'],
        is_restricted=user['is_restricted'],
        last_updated=datetime.now(),
        playmode=user['playmode'],
        registration_date=datetime.now(),
        username=user['username'],
    ))
    db.session.commit()

def store_user_ruleset(data, ruleset, id):
    db.session.add(sc.ruleset_tables[ruleset](
        id=id,
        last_updated=datetime.now(),
        username=data['username'],
        play_count=data['statistics_rulesets'][ruleset]['play_count'],
        play_time=data['statistics_rulesets'][ruleset]['play_time'],
        ranked_score=data['statistics_rulesets'][ruleset]['ranked_score'],
        streak_current=0,
        streak_longest=0,
        total_hits=data['statistics_rulesets'][ruleset]['total_hits'],
        total_score=data['statistics_rulesets'][ruleset]['total_score'],
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
        total_score=0,
    ))
    db.session.commit()

def store_scores(app, access, id, ruleset):
    with app.app_context():
        scores = ft.fetch_scores(access, id, ruleset)
        for score in scores:
            beatmap = score['beatmap']
            beatmapset = score['beatmapset']
            map = rd.read_beatmap(beatmap['id'], beatmapset['id'])
            set = rd.read_beatmapset(beatmapset['id'])
            potential_score = rd.read_score(score['id'])
            if not set:
                store_beatmapset(beatmapset)
            if not map:
                store_beatmap(beatmap)
            if not potential_score:
                store_score(score)
            break

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
    print(score)
    db.session.add(Score(
        id=score['current_user_attributes']['pin']['score_id'],
        user_id=score['user_id'],
        timestamp=score['created_at'],
        ruleset=
        count_300=
        count_100=
        count_50=
        count_geki=
        count_katu=
        count_miss=
        accuracy=
        beatmap_id=
        beatmapset_id=
        max_combo=
        mods=
        passed=
        rank=
        score=
    ))
    return

def update_user_statistics(app, user):
    with app.app_context():

        updated_statistics = ft.fetch_user(user.__dict__['access_token'])
        id = updated_statistics['id']

        for ruleset in sc.rulesets:
            old_ruleset = rd.read_ruleset(id, ruleset)

            if not old_ruleset:
                store_user_ruleset(updated_statistics, ruleset, id)
                store_user_daily(ruleset, id)
            else:

                # heatmap cell
                
                old_cell = rd.read_cell(id, ruleset, date.today())
                if not old_cell:
                    store_user_daily(ruleset, id)
                else:
                    setattr(old_cell, 'play_time', (updated_statistics['statistics_rulesets'][ruleset]['play_time'] - old_ruleset.__dict__['play_time']) + getattr(old_cell, 'play_time'))
                    
                    setattr(old_cell, 'play_count', (updated_statistics['statistics_rulesets'][ruleset]['play_count'] - old_ruleset.__dict__['play_count']) + getattr(old_cell, 'play_count'))
                    
                    setattr(old_cell, 'total_hits', (updated_statistics['statistics_rulesets'][ruleset]['total_hits'] - old_ruleset.__dict__['total_hits']) + getattr(old_cell, 'total_hits'))
                    
                    setattr(old_cell, 'ranked_score', (updated_statistics['statistics_rulesets'][ruleset]['ranked_score'] - old_ruleset.__dict__['ranked_score']) + getattr(old_cell, 'ranked_score'))
                    
                    setattr(old_cell, 'total_score', (updated_statistics['statistics_rulesets'][ruleset]['total_score'] - old_ruleset.__dict__['total_score']) + getattr(old_cell, 'total_score'))
                    

                # todo: update ruleset attributes for everything except streaks using collection above
                
                # ruleset

                setattr(old_ruleset, 'last_updated', datetime.now())
                setattr(old_ruleset, 'username', updated_statistics['username'])
                setattr(old_ruleset, 'play_count', updated_statistics['statistics_rulesets'][ruleset]['play_count'])
                setattr(old_ruleset, 'play_time', updated_statistics['statistics_rulesets'][ruleset]['play_time'])
                setattr(old_ruleset, 'ranked_score', updated_statistics['statistics_rulesets'][ruleset]['ranked_score'])
                setattr(old_ruleset, 'total_hits', updated_statistics['statistics_rulesets'][ruleset]['total_hits'])
                setattr(old_ruleset, 'total_score', updated_statistics['statistics_rulesets'][ruleset]['total_score'])

                db.session.commit()
