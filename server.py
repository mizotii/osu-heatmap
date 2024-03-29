from config import Config, Endpoints
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)

@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')

@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

@app.route("/config")
def get_config(key):
    return

if __name__ == "__main__":
    app.run(debug = True)