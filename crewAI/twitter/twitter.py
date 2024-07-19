import base64
import hashlib
import os
import re
import json
import requests
from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for,render_template
from dotenv import load_dotenv
from .crew import Twitter
import sys

load_dotenv()

class TwitterAutoPoster:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = os.urandom(50)
        self.client_id = os.environ.get("TWITTER_OAUTH_CLIENT_ID")
        self.client_secret = os.environ.get("TWITTER_OAUTH_CLIENT_SECRET")
        self.auth_url = "https://twitter.com/i/oauth2/authorize"
        self.token_url = "https://api.twitter.com/2/oauth2/token"
        self.redirect_uri = os.environ.get("REDIRECT_URI")

        self.scopes = ["tweet.read", "users.read", "tweet.write", "offline.access"]

        self.code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
        self.code_verifier = re.sub("[^a-zA-Z0-9]+", "", self.code_verifier)

        self.code_challenge = hashlib.sha256(self.code_verifier.encode("utf-8")).digest()
        self.code_challenge = base64.urlsafe_b64encode(self.code_challenge).decode("utf-8")
        self.code_challenge = self.code_challenge.replace("=", "")

        self.app.add_url_rule("/", "index", self.demo)
        self.app.add_url_rule("/oauth/callback", "callback", self.callback, methods=["GET"])
        self.app.add_url_rule("/logout", "logout", self.logout)

        self.twitter = None
        self.generated_tweet = None

    def make_token(self):
        return OAuth2Session(self.client_id, redirect_uri=self.redirect_uri, scope=self.scopes)

    def post_tweet(self):
        with open("twitter_access_token.json", "r") as token_file:
            self.token = json.load(token_file)
        
        self.generated_tweet = self.generate_tweet()
        if not self.generated_tweet:
            return "Failed to generate tweet content."

        max_tweet_length = 280
        if len(self.generated_tweet) > max_tweet_length:
            self.generated_tweet = self.generated_tweet[:max_tweet_length - 3] + '...'

        payload = {"text": self.generated_tweet}
        
        print("Tweeting!")
        response = requests.request(
            "POST",
            "https://api.twitter.com/2/tweets",
            json=payload,
            headers={
                "Authorization": f"Bearer {self.token['access_token']}",
                "Content-Type": "application/json",
            },
        )
        return response

    def generate_tweet(self):
        twitter_instance = Twitter()  
        result = twitter_instance.run()
        # result = "Testing Tweet"
        print("Generated Tweet:", result)
        return result

    def demo(self):
        if "oauth_state" in session:
            self.post_tweet()
            return render_template("index.html",user_info = self.user_info)
        else :
            self.twitter = self.make_token()
            authorization_url, state = self.twitter.authorization_url(
                self.auth_url, code_challenge=self.code_challenge, code_challenge_method="S256"
            )
            session["oauth_state"] = state
            print(f"Authorization URL: {authorization_url}")
            print(f"OAuth State: {state}")
    
            return render_template("index.html",authorization_url=authorization_url)
    
    def callback(self):
        code = request.args.get("code")
        token = self.twitter.fetch_token(
            token_url=self.token_url,
            client_secret=self.client_secret,
            code_verifier=self.code_verifier,
            code=code,
        )
        fields = "id,username,name,description,profile_image_url,location,url,verified"
        params = {"user.fields": fields}
        session['oauth_state'] = token
        self.user_info = self.twitter.get('https://api.twitter.com/2/users/me', params=params)
        print("Response status code:", self.user_info.status_code)
        print("Response headers:", self.user_info.headers)
        print("Raw response content:", self.user_info.content)
        self.user_info = self.user_info.json()
        with open("twitter_access_token.json", "w") as token_file:
            json.dump(token, token_file)
        return redirect("/")

    def logout(self):
        session.clear()
        return redirect("/")
   
    def run(self):
        self.app.run()


