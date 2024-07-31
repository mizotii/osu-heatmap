import os
from server_config import credentials
from urllib.parse import urlencode, urljoin

endpoints = {
    'oauth': 'https://osu.ppy.sh/oauth/authorize',
    'callback': 'http://localhost:5000/callback',
}

query_params = {
    'client_id': credentials['client_id'],
    'redirect_uri': endpoints['callback'],
    'response_type': 'code',
    'scope': 'public identify',
    'state': 'randomval',
}

def build_url():
    params = urlencode(query_params)
    return urljoin(endpoints['oauth'], '?' + params)