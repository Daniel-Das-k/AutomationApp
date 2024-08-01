# import os
# from flask import Flask, redirect, url_for
# from flask_dance.contrib.twitter import make_twitter_blueprint, twitter

# app = Flask(__name__)
# app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
# app.config["TWITTER_OAUTH_CLIENT_ID"] = os.environ.get("TWITTER_OAUTH_CLIENT_ID")
# app.config["TWITTER_OAUTH_CLIENT_SECRET"] = os.environ.get("TWITTER_OAUTH_CLIENT_SECRET")
# twitter_bp = make_twitter_blueprint()
# app.register_blueprint(twitter_bp, url_prefix="/login")

# @app.route("/")
# def index():
#     if not twitter.authorized:
#         return redirect(url_for("twitter.login"))
#     resp = twitter.get("account/verify_credentials.json")
#     assert resp.ok
#     return "You are @{screen_name} on Twitter".format(screen_name=resp.json()["screen_name"])


import base64
import hashlib
import os
import re
import json
import requests
from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for, render_template

app = Flask(__name__)
app.secret_key = os.urandom(50)
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
auth_url = "https://twitter.com/i/oauth2/authorize"
token_url = "https://api.twitter.com/2/oauth2/token"
redirect_uri = os.environ.get("REDIRECT_URI")

scopes = ["tweet.read", "users.read", "tweet.write", "offline.access"]

code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
code_verifier = re.sub("[^a-zA-Z0-9]+", "", code_verifier)
code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
code_challenge = code_challenge.replace("=", "")

def make_token():
    return OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)

def post_tweet(payload, token):
    print("Tweeting!")
    return requests.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
        headers={
            "Authorization": f"Bearer {token['access_token']}",
            "Content-Type": "application/json",
        },
    )

@app.route("/")
def demo():
    global twitter
    twitter = make_token()
    authorization_url, state = twitter.authorization_url(
        auth_url, code_challenge=code_challenge, code_challenge_method="S256"
    )
    session["oauth_state"] = state
    return redirect(authorization_url)

@app.route("/oauth/callback", methods=["GET"])
def callback():
    code = request.args.get("code")
    token = twitter.fetch_token(
        token_url=token_url,
        client_secret=client_secret,
        code_verifier=code_verifier,
        code=code,
    )
    with open("twitter_access_token.json", "w") as token_file:
        json.dump(token, token_file)

    payload = {"text": "Hello, world! This is a test tweet from the Flask app."}
    response = post_tweet(payload, token)
    return response.text

if __name__ == "__main__":
    app.run()
