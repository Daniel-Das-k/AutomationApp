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
#     page_access_token = session.get("page_access_token")
#     if access_token and page_access_token:
#         return f'''
#             User Access Token: {access_token}
#             Page Access Token: {page_access_token}
#         '''
#     else:
#         return redirect(url_for('facebook_login'))

# @app.route('/facebook/login')
# def facebook_login():
#     return redirect(f"https://www.facebook.com/v20.0/dialog/oauth?client_id={Fb_APP_ID}&redirect_uri={Fb_REDIRECT_URI}&scope=read_insights,publish_video,pages_manage_instant_articles,pages_show_list,pages_messaging,instagram_basic,instagram_manage_comments,instagram_manage_insights,instagram_content_publish,page_events,pages_read_engagement,pages_read_user_content,pages_manage_metadata,pages_manage_posts,pages_manage_engagement,instagram_manage_events")

# @app.route('/facebook/callback')
# def facebook_callback():
#     code = request.args.get("code")
#     if code:
#         response = requests.get(
#             f"https://graph.facebook.com/v20.0/oauth/access_token?client_id={Fb_APP_ID}&redirect_uri={Fb_REDIRECT_URI}&client_secret={Fb_APP_SECRET}&code={code}"
#         )
#         print("Response: ",response)
#         data = response.json()
#         if "access_token" in data:
#             user_access_token = data["access_token"]
#             session["access_token"] = user_access_token

#             pages_response = requests.get(
#                 f"https://graph.facebook.com/v20.0/me/accounts?access_token={user_access_token}"
#             )
#             pages_data = pages_response.json()
#             if 'data' in pages_data:
#                 print("Pages Data :",pages_data)
#                 first_page = pages_data['data'][0]
#                 page_access_token = first_page['access_token']
#                 session["page_access_token"] = page_access_token
#                 session["page_id"] = first_page['id']
#                 return redirect(url_for('home'))
#             else:
#                 error_message = pages_data.get('error', {}).get('message', 'Unknown error')
#                 return f"Error fetching pages: {error_message}"
#         else:
#             error_message = data.get('error', {}).get('message', 'Unknown error')
#             return f"Error fetching user access token: {error_message}"
#     else:
#         return "Error: No code provided or invalid code"


# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5002))
#     app.run(host='0.0.0.0', port=port)


import os
import json
from flask import Flask, redirect, request, session, url_for, render_template
import requests

class FacebookOauth:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = "secret"
        self.Fb_APP_ID = os.getenv('FB_APP_ID')
        self.Fb_APP_SECRET = os.getenv('FB_APP_SECRET')
        self.Fb_REDIRECT_URI = os.getenv('FB_REDIRECT_URI')
        self.token_file = 'facebook_token.json'
        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/', 'home', self.home)
        self.app.add_url_rule('/facebook/login', 'facebook_login', self.facebook_login)
        self.app.add_url_rule('/facebook/callback', 'facebook_callback', self.facebook_callback)
        self.app.add_url_rule('/logout', 'logout', self.logout)

    def home(self):
        stored_data = self.get_stored_data()
        if stored_data:
            access_token = stored_data.get("access_token")
            page_access_token = stored_data.get("page_access_token")
            if access_token and page_access_token:
                return f'''
                    User Access Token: {access_token}<br>
                    Page Access Token: {page_access_token}
                '''
        return redirect(url_for('facebook_login'))

    def facebook_login(self):
        auth_url = (f"https://www.facebook.com/v20.0/dialog/oauth"
                    f"?client_id={self.Fb_APP_ID}&"
                    f"redirect_uri={self.Fb_REDIRECT_URI}&"
                    f"scope=read_insights,publish_video,"
                    f"pages_manage_instant_articles,pages_show_list,"
                    f"pages_messaging,instagram_basic,instagram_manage_comments,"
                    f"instagram_manage_insights,instagram_content_publish,"
                    f"page_events,pages_read_engagement,pages_read_user_content,"
                    f"pages_manage_metadata,pages_manage_posts,"
                    f"pages_manage_engagement,instagram_manage_events")
        return redirect(auth_url)

    def facebook_callback(self):
        code = request.args.get("code")
        if code:
            response = requests.get(
                f"https://graph.facebook.com/v20.0/oauth/access_token"
                f"?client_id={self.Fb_APP_ID}&"
                f"redirect_uri={self.Fb_REDIRECT_URI}&"
                f"client_secret={self.Fb_APP_SECRET}&"
                f"code={code}"
            )
            data = response.json()
            if "access_token" in data:
                user_access_token = data["access_token"]
                pages_response = requests.get(
                    f"https://graph.facebook.com/v20.0/me/accounts"
                    f"?access_token={user_access_token}"
                )
                pages_data = pages_response.json()
                if 'data' in pages_data and pages_data['data']:
                    first_page = pages_data['data'][0]
                    page_access_token = first_page['access_token']
                    self.store_data({
                        "access_token": user_access_token,
                        "page_access_token": page_access_token
                    })
                    return redirect(url_for('home'))
                else:
                    error_message = pages_data.get('error', {}).get('message', 'Unknown error')
                    return f"Error fetching pages: {error_message}"
            else:
                error_message = data.get('error', {}).get('message', 'Unknown error')
                return f"Error fetching user access token: {error_message}"
        return "Error: No code provided or invalid code"

    def logout(self):
        if os.path.exists(self.token_file):
            os.remove(self.token_file)
        session.clear()
        return redirect(url_for('home'))

    def get_stored_data(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as f:
                return json.load(f)
        return None

    def store_data(self, data):
        print("In Store_data Function")
        with open(self.token_file, 'w') as f:
            json.dump(data, f)

    def run(self, debug=True):
        port = int(os.environ.get("PORT", 5002))
        self.app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == "__main__":
    app = FacebookOauth()
    app.run()

