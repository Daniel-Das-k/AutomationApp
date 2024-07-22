
from flask import Flask, redirect, request, session, url_for
import requests
import os
import json

app = Flask(__name__)
app.secret_key = "secret"
Fb_APP_ID = "1519269175630468"
Fb_APP_SECRET = "e04ebcfe52882ed9a9134937547e0ba0"
Fb_REDIRECT_URI = "https://facebook-rakb.onrender.com/facebook/callback"

@app.route('/')
def home():  
    access_token = session.get("access_token")
    print(access_token)
    if access_token:
        return f"Access Token: {access_token}"
    else:
        return "Home Page"

@app.route('/facebook/login')
def facebook_login():
    print("Facebook login route accessed")
    return redirect(f"https://www.facebook.com/v12.0/dialog/oauth?client_id={Fb_APP_ID}&redirect_uri={Fb_REDIRECT_URI}&scope=read_insights")

@app.route('/facebook/callback')
def facebook_callback():
    print("Facebook callback route accessed")
    code = request.args["code"]
    if code:
        response = requests.get(
            f"https://graph.facebook.com/v12.0/oauth/access_token?client_id={Fb_APP_ID}&redirect_uri={Fb_REDIRECT_URI}&client_secret={Fb_APP_SECRET}&code={code}"
        )
        data = response.json()
        print("Response from Facebook:", data)
        if "access_token" in data:
            access_token = data["access_token"]
            session["access_token"] = access_token
            print("Access token obtained:", access_token)

            try:
                with open('access_token.json', 'w') as token_file:
                    json.dump({"access_token": access_token}, token_file)
                print("Access token saved to access_token.json")
            except Exception as e:
                print("Error writing to access_token.json:", e)

            user_response = requests.get(
                f"https://graph.facebook.com/v12.0/me?fields=id,name,email&access_token={access_token}"
            )
            print("User response:", user_response.json())
            return redirect(url_for('home'))
    else:
        return "Error: No code provided or invalid code"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port)
