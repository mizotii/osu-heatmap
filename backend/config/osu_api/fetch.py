from config.server_config import endpoints, headers
from db import read as rd
from urllib.parse import urlencode, urljoin
import requests

# get own data
def fetch_self(access, ruleset=None):
    auth = 'Bearer {}'
    headers['Authorization'] = auth.format(access)
    if ruleset:
        r = requests.get(endpoints['v2'] + endpoints[ruleset], headers=headers)
    else:
        r = requests.get(endpoints['v2'] + endpoints['self'], headers=headers)
    return r.json()

# get user data
def fetch_user(id, ruleset=None):
    access = rd.read_client_credentials().__dict__['access_token']
    auth = 'Bearer {}'
    headers['Authorization'] = auth.format(access)
    endpoint = f'/users/{id}'
    if ruleset:
        endpoint += f'/{ruleset}'
    r = requests.get(endpoints['v2'] + endpoint, headers=headers)
    return r.json()

def fetch_scores(id, ruleset):
    access = rd.read_client_credentials().__dict__['access_token']
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