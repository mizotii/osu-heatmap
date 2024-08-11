from db import read as rd
from datetime import datetime

def create_profile(id, ruleset):
    user = rd.read_user(id).as_dict()
    user_ruleset = rd.read_ruleset(id, ruleset).as_dict()
    user_cells = rd.all_cells_for_user(id, ruleset)

    data = []
    if user_cells:
        for cell in user_cells:
            data.append(cell.as_dict())
    return {
        'user': {
            'avatar_url': user['avatar_url'],
            'country_code': user['country_code'],
            'playmode': user['playmode'],
            'username': user['username'],
        },
        'user_ruleset': user_ruleset,
        'user_heatmap_data': data,
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
