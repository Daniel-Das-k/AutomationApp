from flask import Flask, redirect, request, session, url_for, render_template
import requests
import os
import json

class FacebookOAuthApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = "secret"
        self.Fb_APP_ID = "1519269175630468"
        self.Fb_APP_SECRET = "e04ebcfe52882ed9a9134937547e0ba0"
        self.Fb_REDIRECT_URI = "https://facebook-rakb.onrender.com/facebook/callback"
        self.TOKEN_FILE = 'access_token.json'
        
        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/', 'home', self.home)
        self.app.add_url_rule('/facebook/login', 'facebook_login', self.facebook_login)
        self.app.add_url_rule('/facebook/callback', 'facebook_callback', self.facebook_callback)
        self.app.add_url_rule('/logout', 'logout', self.logout)

    def home(self):
        stored_data = self.get_stored_data()
        if stored_data:
            access_token = stored_data['access_token']
            print("Access Token loaded from storage:", access_token)
            # Optionally fetch and display user data from Facebook API
            user_data = self.get_user_data(access_token)
            return render_template("index.html", user_data=user_data)
        else:
            return render_template("index.html", oauth_uri=self.get_oauth_url())

    def facebook_login(self):
        print("Facebook login route accessed")
        return redirect(self.get_oauth_url())

    def facebook_callback(self):
        print("Facebook callback route accessed")
        code = request.args.get("code")
        if code:
            response = requests.get(
                f"https://graph.facebook.com/v12.0/oauth/access_token?client_id={self.Fb_APP_ID}&redirect_uri={self.Fb_REDIRECT_URI}&client_secret={self.Fb_APP_SECRET}&code={code}"
            )
            data = response.json()
            if "access_token" in data:
                access_token = data["access_token"]
                self.store_data({
                    'access_token': access_token
                })
                
                user_data = self.get_user_data(access_token)
                print("User response", user_data)
                return redirect(url_for('home'))
        else:
            return "Error: No code provided or invalid code"

    def logout(self):
        session.clear()
        if os.path.exists(self.TOKEN_FILE):
            os.remove(self.TOKEN_FILE)
        return redirect("/")

    def get_oauth_url(self):
        return f"https://www.facebook.com/v12.0/dialog/oauth?client_id={self.Fb_APP_ID}&redirect_uri={self.Fb_REDIRECT_URI}&scope=email"

    def get_stored_data(self):
        if os.path.exists(self.TOKEN_FILE):
            with open(self.TOKEN_FILE, 'r') as f:
                return json.load(f)
        return None

    def store_data(self, data):
        with open(self.TOKEN_FILE, 'w') as f:
            json.dump(data, f)

    def get_user_data(self, access_token):
        user_response = requests.get(
            f"https://graph.facebook.com/v12.0/me?fields=id,name,email&access_token={access_token}"
        )
        return user_response.json()

    def run(self):
        port = int(os.environ.get("PORT", 5001))
        self.app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    app = FacebookOAuthApp()
    app.run()


# from flask import Flask, redirect, request, session, url_for
# import requests
# import os
# import json

# class FacebookOAuthApp:
#     def __init__(self):
#         self.app = Flask(__name__)
#         self.app.secret_key = "secret"
#         self.Fb_APP_ID = "1519269175630468"
#         self.Fb_APP_SECRET = "e04ebcfe52882ed9a9134937547e0ba0"
#         self.Fb_REDIRECT_URI = "https://facebook-rakb.onrender.com/facebook/callback"
        
#         self.setup_routes()

#     def setup_routes(self):
#         self.app.add_url_rule('/', 'home', self.home)
#         self.app.add_url_rule('/facebook/login', 'facebook_login', self.facebook_login)
#         self.app.add_url_rule('/facebook/callback', 'facebook_callback', self.facebook_callback)

#     def home(self):
#         access_token = session.get("access_token")
#         print(access_token)
#         if access_token:
#             return f"Access Token: {access_token}"
#         else:
#             return "Home Page"

#     def facebook_login(self):
#         print("Facebook login route accessed")
#         return redirect(f"https://www.facebook.com/v12.0/dialog/oauth?client_id={self.Fb_APP_ID}&redirect_uri={self.Fb_REDIRECT_URI}&scope=read_insights")

#     def facebook_callback(self):
#         print("Facebook callback route accessed")
#         code = request.args.get("code")
#         if code:
#             response = requests.get(
#                 f"https://graph.facebook.com/v12.0/oauth/access_token?client_id={self.Fb_APP_ID}&redirect_uri={self.Fb_REDIRECT_URI}&client_secret={self.Fb_APP_SECRET}&code={code}"
#             )
#             data = response.json()
#             if "access_token" in data:
#                 access_token = data["access_token"]
#                 session["access_token"] = access_token

#                 with open('access_token.json', 'w') as token_file:
#                     json.dump({"access_token": access_token}, token_file)

#                 user_response = requests.get(
#                     f"https://graph.facebook.com/v12.0/me?fields=id,name,email&access_token={access_token}"
#                 )
#                 print("User response", user_response.json())
#                 return redirect(url_for('home'))
#         else:
#             return "Error: No code provided or invalid code"

#     def run(self):
#         port = int(os.environ.get("PORT", 5001))
#         self.app.run(host='0.0.0.0', port=port)

# if __name__ == "__main__":
#     app = FacebookOAuthApp()
#     app.run()
