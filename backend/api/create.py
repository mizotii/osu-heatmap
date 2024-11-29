from config import server_config as sc
from db import read as rd
from datetime import datetime, timedelta

def create_profile(id, ruleset, isOverall):
    user = rd.read_user(id).as_dict()

    if not isOverall:
        user_ruleset = rd.read_ruleset(id, ruleset).as_dict()
        user_cells = rd.all_cells_for_user(id, ruleset)
        heatmap_max = rd.read_max_statistic(id, ruleset)
        heatmap_data = []

        if user_cells:
            for cell in user_cells:
                if cell.__dict__['play_count'] != 0:
                    heatmap_data.append(cell.as_dict())
        # needs refactoring, return statements literally the same
        return {
            'user': {
                'avatar_url': user['avatar_url'],
                'country_code': user['country_code'],
                'playmode': user['playmode'],
                'registration_date': user['registration_date'].strftime("%b %d %Y").upper(),
                'username': user['username'],
            },
            'user_ruleset': user_ruleset,
            'user_heatmap_data': heatmap_data,
            'user_heatmap_max': heatmap_max,
        }
    else:
        heatmap_data, heatmap_max, user_ruleset = create_overall_data(user)
        return {
            'user': {
                'avatar_url': user['avatar_url'],
                'country_code': user['country_code'],
                'playmode': user['playmode'],
                'registration_date': user['registration_date'].strftime("%b %d %Y").upper(),
                'username': user['username'],
            },
            'user_ruleset': user_ruleset,
            'user_heatmap_data': heatmap_data,
            'user_heatmap_max': heatmap_max,
        }

def create_score_list(id, ruleset, timestamp):
    start = datetime.fromtimestamp(timestamp / 1000)
    data_banners = rd.all_scores_on_day(id, ruleset, start)
    scores = []
    if data_banners:
        for score, beatmap, beatmapset in data_banners:
            scores.append({
                'score_data': score.as_dict(),
                'beatmap_data': beatmap.as_dict(),
                'beatmapset_data': beatmapset.as_dict(),
            })
    return scores

def create_overall_data(user):
    id = user['id']
    reg = user['registration_date'].replace(hour=0, minute=0, second=0, microsecond=0)

    overall = []
    user_ruleset = {
        'accumulated_play_count': 0,
        'accumulated_play_time': 0,
        'accumulated_ranked_score': 0,
        'accumulated_total_hits': 0,
        'accumulated_total_score': 0,

        'streak_current': user['streak_current'],
        'streak_longest': user['streak_longest'],
    }
    overall_max = {
        'play_count': 0,
        'play_time': 0,
        'ranked_score': 0,
        'total_hits': 0,
        'total_score': 0,
    }

    for ruleset in sc.rulesets:
        ruleset_stats = rd.read_ruleset(id, ruleset).as_dict()
        user_ruleset['accumulated_play_count'] += ruleset_stats['accumulated_play_count']
        user_ruleset['accumulated_play_time'] += ruleset_stats['accumulated_play_time']
        user_ruleset['accumulated_ranked_score'] += ruleset_stats['accumulated_ranked_score']
        user_ruleset['accumulated_total_hits'] += ruleset_stats['accumulated_total_hits']
        user_ruleset['accumulated_total_score'] += ruleset_stats['accumulated_total_score']

    for i in range((datetime.today() - reg).days):
        start_date = reg + timedelta(days = i + 1)
        overall_cell = {
            'id': id,
            'ruleset': 'overall',
            'start_date': start_date,
        }
        for statistic in sc.daily_statistics:
            sum = rd.read_summed_statistic(id, start_date, statistic)
            if sum:
                if sum > overall_max[statistic]:
                    overall_max[statistic] = sum
                overall_cell[statistic] = int(sum)
        overall.append(overall_cell)

    return overall, overall_max, user_ruleset