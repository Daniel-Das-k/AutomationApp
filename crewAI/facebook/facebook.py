import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["FACEBOOK_OAUTH_CLIENT_ID"] = os.environ.get("FACEBOOK_OAUTH_CLIENT_ID")
app.config["FACEBOOK_OAUTH_CLIENT_SECRET"] = os.environ.get("FACEBOOK_OAUTH_CLIENT_SECRET")
facebook_bp = make_facebook_blueprint()
app.register_blueprint(facebook_bp, url_prefix="/login")

@app.route("/")
def index():
    if not facebook.authorized:
        return redirect(url_for("facebook.login"))
    resp = facebook.get("/me")
    assert resp.ok, resp.text
    return "You are {name} on Facebook".format(name=resp.json()["name"])

if __name__ == "__main__":
    app.run()


# import os
# import json
# from flask import Flask, redirect, url_for, session, render_template
# from dotenv import load_dotenv
# from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
# from flask_cors import CORS
# load_dotenv()
# # Initialize Flask app

# class FaceBookOAuthApp:
#     def __init__(self):
#         self.app = Flask(__name__)
#         self.app.config["SECRET_KEY"] = "SECRET_KEY"

#         self.facebook_bp = make_facebook_blueprint(
#             client_id=os.environ.get["FACEBOOK_OAUTH_CLIENT_ID"],
#             client_secret=os.environ.get["FACEBOOK_OAUTH_CLIENT_SECRET"],
#         )
#         self.app.register_blueprint(self.facebook_bp, url_prefix="/facebook_login")
#         self.setup_routes()

#     def setup_routes(self):
#         self.app.add_url_rule('/','index',self.index)
#         self.app.add_url_rule('/logout','logout',self.logout)

#     def index(self):
#         if facebook.authorized:
#             account_info = facebook.get("/me?fields=id,name,email")
#             if account_info.ok:
#                 account_info_json= account_info.json()
#                 return render_template("index.html",user_info=account_info_json)

#         else:
#             return render_template("index.html",facebook_url = url_for('facebook.login'))


#     def logout(self):
#         # Clear the session and remove the access token file
#         session.clear()
#         return redirect('/')
    
#     def run(self,debug=True):
#         self.app.run(debug=debug)
    

# if __name__ == "__main__":
#     facebook_oauth_app = FaceBookOAuthApp()
#     facebook_oauth_app.run()


# from flask import Flask, redirect, request, session, url_for
# import requests
# import os
# import json

# app = Flask(__name__)
# app.secret_key = "secret"
# Fb_APP_ID = "1519269175630468"
# Fb_APP_SECRET = "e04ebcfe52882ed9a9134937547e0ba0"
# Fb_REDIRECT_URI = "https://facebook-rakb.onrender.com/facebook/callback"

# @app.route('/')
# def home():
    
#     access_token = session.get("access_token")
#     if access_token:
        
#         return f"Access Token: {access_token}"
#     else:
#         return "Home Page"

# @app.route('/facebook/login')
# def facebook_login():
#     print("Facebook login route accessed")
#     return redirect(f"https://www.facebook.com/v12.0/dialog/oauth?client_id={Fb_APP_ID}&redirect_uri={Fb_REDIRECT_URI}&scope=read_insights")

# @app.route('/facebook/callback')
# def facebook_callback():
#     print("Facebook callback route accessed")
#     code = request.args["code"]
#     if code:
#         response = requests.get(
#             f"https://graph.facebook.com/v12.0/oauth/access_token?client_id={Fb_APP_ID}&redirect_uri={Fb_REDIRECT_URI}&client_secret={Fb_APP_SECRET}&code={code}"
#         )
#         data = response.json()
#         print("Response from Facebook:", data)
#         if "access_token" in data:
#             access_token = data["access_token"]
#             session["access_token"] = access_token
#             print("Access token obtained:", access_token)

#             try:
#                 with open('access_token.json', 'w') as token_file:
#                     json.dump({"access_token": access_token}, token_file)
#                 print("Access token saved to access_token.json")
#             except Exception as e:
#                 print("Error writing to access_token.json:", e)

#             user_response = requests.get(
#                 f"https://graph.facebook.com/v12.0/me?fields=id,name,email&access_token={access_token}"
#             )
#             print("User response:", user_response.json())
#             return redirect(url_for('home'))
#     else:
#         return "Error: No code provided or invalid code"

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5001))
#     app.run(host='0.0.0.0', port=port)
