from config import Config
from flask import Flask, redirect, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, User, APIToken
import requests, os


# app / db config
app = Flask(__name__)
app.config.from_object(Config)
app.config["SQLALCHEMY_DATABASE_URI"] = Config.OH_DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
migrate = Migrate(app, db, compare_type=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/authorize")
def authorize():
    return redirect(Config.AUTH_URL)


@app.route("/callback")
def callback():
    code = request.args.get('code')
    if code:
        token_headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        token_data = {
            "client_id": Config.CLIENT_ID,
            "client_secret": Config.CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": Config.REDIRECT_URI
        }
        token_response = requests.post(Config.TOKEN_URL, headers=token_headers, data=token_data).json()
        access_id = token_response.get("access_token")
        refresh_id = token_response.get("refresh_token")
        user_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {access_id}"
        }
        user_response = requests.get(Config.REQUEST_USER_URL, headers=user_headers).json()
        user_id = user_response.get("id")
        username = user_response.get("username")
        new_token = APIToken(access_id=access_id, refresh_id=refresh_id, user_id=user_id)
        new_user = User(id=user_id, username=username)
        db.session.add(new_user)
        db.session.add(new_token)
        db.session.commit()
        
        return redirect("success.html")
    else:
        return redirect("templates/failure.html")


if __name__ == "__main__":
    app.run(debug=True)