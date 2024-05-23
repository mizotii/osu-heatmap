from datetime import datetime
import requests
from urllib.parse import urlencode, urljoin

def create_headers(token=None):
    headers = {
        'Accept': 'application/json',
    }
    if token:
        headers['Content-Type'] = 'application/json'
        headers['Authorization'] = f'Bearer {token}'
    else:
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
    return headers

def create_recents_endpoint(id):
    return f'/users/{id}/scores/recent'

def create_recents_parameters(ruleset):
    params = {
        'include_fails': '1',
        'limit': 999,
        'mode': ruleset,
    }
    return params

access = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMDMyNiIsImp0aSI6ImJkN2RhZmI0ZDkzNmRlNzNkMTA0YTdmMTc0NTRiMjQ3NjQ3ZTgxMWFhMjFhZTY5MjZhMDZlNjg1ZTFlODMxNTM0OGFiMmUwNTJjZTFkNzRiIiwiaWF0IjoxNzE1NjYxNDQ4LjMwMTExNCwibmJmIjoxNzE1NjYxNDQ4LjMwMTExNSwiZXhwIjoxNzE1NzQ3ODQ4LjI4OTQ1LCJzdWIiOiI4ODE2ODQ0Iiwic2NvcGVzIjpbImlkZW50aWZ5IiwicHVibGljIl19.b_RTOF1TQfPmOMvXrqF4G_6mhQusQMMOLcB9BP7Tm5E2qj-Be1OTo5hmC58IcEbhTHpHv-vj08L5gmQYAZtR7tiOzulBrDGh3qfPZtruXbZoZXn2VzCiuuPbBTyvjoaOzfEoG2KC-rHMq4VNoOeaYayV5-NKUM_DoiWeYP_cBNx6Gze1ngKxBEfNwN1NZqGErGqxp53Kbexfbwp_HHvbTLS4XT1qI8AtmnRlOIVHlWMD4pzurp8XwX3QAhVPlsxRFc_Ren4bFmLT7JMlZeKwuVPF6PRzlNdBvsJ-DuHy9uaGR-BFwGRFOZp5wkaOThN4EEy_BgRFGhp0z6GvUM88hSD3irLGBng5X1sw8HxFcbSpxFm9jkvITRN-BvpounbADxDcYWTpz20wRAswr-z0oumiI6iC264LQZ2jZI0pdUU_AXWoOyHHTM713GMC1b7c9AaqMUzB8ijUh0XTU0LAC8plSDEuAZmPxKLVk-4mWVOtlCZiM_w70YUurbAh0N0VO8e0gOxlK_S8OtjLgDM8R4P_f4GHtTt4OX3w0Qidxt4pOA9qKu_fGmwjFQpPJMkV7JiGFZih4PoP1Hi9gknmKNPekJhEobEYCRSs_TgM2fz5nSBwU09W57EUTfrsTfUUb2QhpG6c9N-ErqRWDSElERXpdcmLDooBlKNXxbQTgTc'
response = requests.get(
    'https://osu.ppy.sh/api/v2' + urljoin(create_recents_endpoint('8816844'), '?' + urlencode(create_recents_parameters('taiko'))),
    headers=create_headers(access)
)
print(response.json())
print(len(response.json()))