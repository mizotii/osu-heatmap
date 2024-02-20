from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import requests, os

# app config
app = Flask(__name__)

# db config
OH_DB_URI = os.environ.get("OH_DB_URI")
app.config["SQLALCHEMY_DATABASE_URI"] = OH_DB_URI
db = SQLAlchemy(app)

CLIENT_ID = os.environ.get("OH_CLIENT_ID")
CLIENT_SECRET = os.environ.get("OH_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000/callback"
AUTH_URL = f"https://osu.ppy.sh/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=public+identify&state=randomval"
TOKEN_URL = "https://osu.ppy.sh/oauth/token"

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/authorize")
def authorize():
    return redirect(AUTH_URL)


@app.route("/callback")
def callback():
    code = request.args.get('code')
    if code:
        token_headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        token_data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI
        }
        token_response = requests.post(TOKEN_URL, headers=token_headers, data=token_data).json()
        
        return redirect("/store_token")

    
@app.route("/store_token", methods=["POST"])
def store_token():
    return


if __name__ == "__main__":
    app.run(debug=True)