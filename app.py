from config import Config
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import requests, os

# app config
app = Flask(__name__)
app.config.from_object(Config)

# db config
app.config["SQLALCHEMY_DATABASE_URI"] = Config.OH_DB_URI
db = SQLAlchemy(app)

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
        db.session.add(token_response)
        db.session.commit()
        
        return redirect("/success.html")
    else:
        return redirect("/failure.html")


if __name__ == "__main__":
    app.run(debug=True)