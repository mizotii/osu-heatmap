from flask import Flask, jsonify, redirect, render_template, request
import requests, os

# app config
app = Flask(__name__)

# need to reconfigure these when i go live
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000"
AUTH_URL = f"https://osu.ppy.sh/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=public+identify&state=randomval"
TOKEN_URL = "https://osu.ppy.sh/oauth/token"

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/authorize")
def authorize():
    return redirect(AUTH_URL)
    
if __name__ == "__main__":
    app.run(debug=True)