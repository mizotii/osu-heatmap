from config.server_config import endpoints, headers
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