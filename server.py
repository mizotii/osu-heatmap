import config
from flask import Flask, jsonify, redirect, send_from_directory
from flask_cors import CORS
import requests

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
    
@app.route("/callback")
def callback():
    try:
        code = requests.args.get('code')
        exchange_token(code)
        return redirect("/")
    except Exception as e:
        return jsonify({'Error': str(e)})

def exchange_token(code):
    token_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

if __name__ == "__main__":
    app.run(debug = True)