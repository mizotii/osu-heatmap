import os
from urllib.parse import urlencode, urljoin

endpoints = {
    'oauth': 'https://osu.ppy.sh/oauth/authorize',
    'callback': 'http://localhost:5000/callback',
}

credentials = {
    'client_id': os.environ.get('CLIENT_ID'),
    'client_secret': os.environ.get('CLIENT_SECRET'),
}

def build_url():
    base = 'https://osu.ppy.sh/oauth/authorize/'
    params = urlencode(
        {
            'client_id': credentials['client_id'],
            'redirect_uri': endpoints['callback'],
            'response_type': 'code',
            'scope': 'public identify',
            'state': 'randomval',
        }
    )
    return urljoin(endpoints['oauth'], '?' + params)