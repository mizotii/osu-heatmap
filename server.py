from config import create_auth_url, database, get_token_data, store_token
from flask import Flask, jsonify, redirect, request, send_from_directory
from flask_cors import CORS
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database['DB_URI']
CORS(app, resources={r"/config": {"origins": "http://localhost:8080"}})
db.init_app(app)

@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')

@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

@app.route("/authorize")
def auth_redirect():
    url = create_auth_url()
    return jsonify(url)
    
@app.route("/callback")
def callback():
    try:
        code = request.args.get('code')
        token_data = get_token_data(code)
        store_token(token_data)
        return redirect("/")
    except Exception as e:
        return jsonify({'Error': str(e)})

if __name__ == "__main__":
    app.run(debug = True)