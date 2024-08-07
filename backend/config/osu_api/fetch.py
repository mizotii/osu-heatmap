from config.server_config import endpoints, headers
from urllib.parse import urlencode, urljoin
import requests

# get User data
def fetch_user(access, ruleset=None):
    auth = 'Bearer {}'
    headers['Authorization'] = auth.format(access)
    if ruleset:
        r = requests.get(endpoints['v2'] + endpoints[ruleset], headers=headers)
    else:
        r = requests.get(endpoints['v2'] + endpoints['user'], headers=headers)
    return r.json()

def fetch_scores(access, id, ruleset):
    auth = 'Bearer {}'
    headers['Authorization'] = auth.format(access)
    endpoint = f'/users/{id}/scores/recent'
    query_params = {
        'include_fails': 1,
        'mode': ruleset,
        'limit': 999,
    }
    r = requests.get(endpoints['v2'] + endpoint, headers=headers, params=query_params)
    return r.json()