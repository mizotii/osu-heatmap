from flask import Flask, render_template, request
import requests, os

app = Flask(__name__)

# need to reconfigure these when i go live
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

if __name__ == "__main__":
    app.run(debug=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/authorize", methods=["GET", "POST"])
def authorize():
    authorization_url = "https://osu.ppy.sh/oauth/authorize"
    authorization_params = {
        "client_id": CLIENT_ID,
        "redirect_uri": "http://localhost:5000",
        "reponse_type": "code",
        "scope": "public identify",
        "state": "randomval"
    }
    authorization_response = requests.get(authorization_url, params=authorization_params)
    authorization_code = request.args.get("code")

    token_url = "https://osu.ppy.sh/oauth/token"
    token_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": authorization_code,
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:5000"
    }
    token_headers = {
        "Application": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }