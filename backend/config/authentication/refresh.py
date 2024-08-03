from config.server_config import credentials, endpoints, headers
import requests

def refresh_token(user):
    url = endpoints['token']
    payload = {
        'client_id': credentials['client_id'],
        'client_secret': credentials['client_secret'],
        'grant_type': 'refresh_token',
        'refresh_token': user.__dict__['refresh_token'],
    }
    r = requests.post(url=url, headers=headers, params=payload)
    
    return