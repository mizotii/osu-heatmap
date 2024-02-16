from flask import Flask, render_template
import requests

app = Flask(__name__)


@app.route("/")
def index():
    client_id = "30326"
    redirect_uri = "http://localhost:5000"
    return render_template("index.html", client_id=client_id, redirect_uri=redirect_uri)