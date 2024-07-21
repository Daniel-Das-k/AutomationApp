# import os
# from flask import Flask, redirect, url_for
# from flask_dance.contrib.facebook import make_facebook_blueprint, facebook

# app = Flask(__name__)
# app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
# app.config["FACEBOOK_OAUTH_CLIENT_ID"] = os.environ.get("FACEBOOK_OAUTH_CLIENT_ID")
# app.config["FACEBOOK_OAUTH_CLIENT_SECRET"] = os.environ.get("FACEBOOK_OAUTH_CLIENT_SECRET")
# app.config["FACEBOOK_OAUTH_REDIRECT_URI"] = "https://facebook-rakb.onrender.com"
# facebook_bp = make_facebook_blueprint(
#     client_id=app.config["FACEBOOK_OAUTH_CLIENT_ID"],
#     client_secret=app.config["FACEBOOK_OAUTH_CLIENT_SECRET"],
#     redirect_to="facebook.login"
# )
# app.register_blueprint(facebook_bp, url_prefix="/login")

# @app.route("/")
# def index():
#     if not facebook.authorized:
#         return redirect(url_for("facebook.login"))
#     resp = facebook.get("/me")
#     assert resp.ok, resp.text
#     return "You are {name} on Facebook".format(name=resp.json()["name"])

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)


# from flask import Flask, url_for,render_template, request,session,redirect
# import requests
# import os 

# app = Flask(__name__)
# app.secret_key = "secret"
# Fb_APP_ID = "1519269175630468"
# Fb_APP_SECRET = "e04ebcfe52882ed9a9134937547e0ba0"
# Fb_REDIRECT_URI = "https://facebook-rakb.onrender.com/facebook/callback"

# @app.route('/')
# def home():
#     return "home Page"

# @app.route('/facebook/login')
# def facebook_login():
#     print("Facebook login route accessed")
#     return redirect(f"https://www.facebook.com/v12.0/dialog/oauth?client_id={Fb_APP_ID}&redirect_uri={Fb_REDIRECT_URI}&scope=read_insights")

# @app.route('/facebook/callback')
# def facebook_callback():
#     print("Facebook callback route accessed")
#     code = request.args.get("code")
#     if code :
#         response = requests.get(
#             f"https://graph.facebook.com/v12.0/oauth/access_token?client_id={Fb_APP_ID}&redirect_uri={Fb_REDIRECT_URI}&client_secret={Fb_APP_SECRET}&code={code}"
#         )
#         data = response.json()
#         if "access_token" in data :
#             session["acces_token"] = data["access_token"]

#             user_response = requests.get(
#                 f"https://graph.facebook.com/v12.0/me?fields=id,name,email&access_token=(data['access_token])"
#             )
#             print("User response",user_response)
#             return redirect('/')
        
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5001))
#     app.run(host='0.0.0.0', port=port)

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
    code = request.args.get("code")
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
                # Save the access token to a JSON file
                file_path = os.path.abspath('access_token.json')
                print(f"Attempting to save access token to {file_path}")
                with open(file_path, 'w') as token_file:
                    json.dump({"access_token": access_token}, token_file)
                print(f"Access token saved to {file_path}")
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
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)
