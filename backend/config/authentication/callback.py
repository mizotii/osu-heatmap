from config.server_config import credentials, endpoints, headers
import requests

def request_token(code):
    url = endpoints['token']
    payload = {
        'client_id': credentials['client_id'],
        'client_secret': credentials['client_secret'],
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': endpoints['callback']
    }
    r = requests.post(url, headers=headers, data=payload)
    return r.json()