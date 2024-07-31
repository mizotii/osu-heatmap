from server_config import credentials

endpoints = {
    'token': 'https://osu.ppy.sh/oauth/token',
}

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
}

body = {
    'client_id': credentials['client_id'],
}