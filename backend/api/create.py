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
        return {
            'user': {
                'avatar_url': user['avatar_url'],
                'country_code': user['country_code'],
                'playmode': user['playmode'],
                'username': user['username'],
            },
            'user_ruleset': user_ruleset,
            'user_heatmap_data': heatmap_data,
            'user_heatmap_max': heatmap_max,
        }
    else:
        heatmap_data, heatmap_max = create_overall_data(user)
        return {
            'user': {
                'avatar_url': user['avatar_url'],
                'country_code': user['country_code'],
                'playmode': user['playmode'],
                'username': user['username'],
            },
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
    overall_max = {
        'play_count': 0,
        'play_time': 0,
        'ranked_score': 0,
        'total_hits': 0,
        'total_score': 0,
    }

    print(range((datetime.today() - reg).days))

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

    return overall, overall_max