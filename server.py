import config
from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)

@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')

@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

@app.route("/config/client_credentials/<key>")
def fetch_credential(key):
    if key in config.client_credentials:
        return jsonify({key: config.client_credentials.get(key)})
    else:
        return jsonify({'Error': 'Invalid Credential.'})
    
@app.route("/config/endpoints/<key>")
def fetch_endpoint(key):
    if key in config.endpoints:
        return jsonify({key: config.endpoints.get(key)})
    else:
        return jsonify({'Error': 'Invalid Endpoint.'})

if __name__ == "__main__":
    app.run(debug = True)