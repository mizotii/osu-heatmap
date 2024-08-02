from config.server_config import endpoints, headers
import requests

# get User data
def fetch_user(access):
    auth = 'Bearer {}'
    headers['Authorization'] = auth.format(access)
    r = requests.get(endpoints['v2'] + endpoints['user'], headers=headers)
    return r.json()