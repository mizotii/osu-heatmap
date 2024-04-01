import config
import requests
from flask import Flask, jsonify, redirect, request, send_from_directory
from flask_cors import CORS
from urllib.parse import urlencode, urljoin

app = Flask(__name__)
CORS(app, resources={r"/config": {"origins": "http://localhost:8080"}})

@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')

@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

@app.route("/config")
def fetch_config():
    try:
        return jsonify(config.data)
    except Exception as e:
        return jsonify({'Error:': str(e)})

@app.route("/authorize")
def auth_redirect():
    url = create_auth_url()
    return jsonify(url)
    
@app.route("/callback")
def callback():
    try:
        code = request.args.get('code')
        exchange_token(code)
        return redirect("/")
    except Exception as e:
        return jsonify({'Error': str(e)})

def create_auth_url():
    payload = {
        'client_id': config.data['client_credentials']['CLIENT_ID'],
        'redirect_uri': config.data['endpoints']['REDIRECT_URI'],
        'response_type': 'code',
        'scope': 'public identify',
        'state': 'randomval',
    }
    query = urlencode(payload)
    url = urljoin(config.data['endpoints']['AUTHORIZATION_URL'], '?' + query)
    return url

def exchange_token(code):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    body = {
        'client_id': config.data['client_credentials']['CLIENT_ID'],
        'client_secret': config.data['client_credentials']['CLIENT_SECRET'],
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': config.data['endpoints']['REDIRECT_URI'],
    }
    response = requests.post(config.data['endpoints']['TOKEN_URL'], headers=headers, data=body)
    return response.json()

if __name__ == "__main__":
    app.run(debug = True)