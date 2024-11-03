import os
import secrets
from config.server_config import credentials, endpoints
from urllib.parse import urlencode, urljoin

query_params = {
    'client_id': credentials['client_id'],
    'redirect_uri': endpoints['callback'],
    'response_type': 'code',
    'scope': 'public identify',
}

def build_url(state):
    query_params['state'] = state
    params = urlencode(query_params)
    return urljoin(endpoints['oauth'], '?' + params)