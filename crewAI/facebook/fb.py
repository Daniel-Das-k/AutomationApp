from flask import Flask, redirect, request, session, url_for
import requests
import os
import json

app = Flask(__name__)
app.secret_key = "secret"
Fb_APP_ID = "1519269175630468"
Fb_APP_SECRET = "e04ebcfe52882ed9a9134937547e0ba0"
Fb_REDIRECT_URI = "https://facebook-rakb.onrender.com/facebook/callback"

CREDENTIALS_FILE = "facebook_token.json"

@app.route('/')
def home():  
    access_token = session.get("access_token")

    if access_token:
        try:
            with open(CREDENTIALS_FILE, "w") as file:
                json.dump({"access_token": access_token}, file)
            return f"Access Token: {access_token}"
        except Exception as e:
            return f"Error writing access token to file: {e}"
    else:
        return "Home Page"

@app.route('/facebook/login')
def facebook_login():
    return redirect(f"https://www.facebook.com/v12.0/dialog/oauth?client_id={Fb_APP_ID}&redirect_uri={Fb_REDIRECT_URI}&scope=read_insights,publish_video,pages_manage_instant_articles,pages_show_list,pages_messaging,instagram_basic,instagram_manage_comments,instagram_manage_insights,instagram_content_publish,page_events,pages_read_engagement,pages_manage_metadata,pages_read_user_content,pages_manage_posts,pages_manage_engagement,instagram_manage_events")

@app.route('/facebook/callback')
def facebook_callback():
    code = request.args.get("code")
    if code:
        response = requests.get(
            f"https://graph.facebook.com/v12.0/oauth/access_token?client_id={Fb_APP_ID}&redirect_uri={Fb_REDIRECT_URI}&client_secret={Fb_APP_SECRET}&code={code}"
        )
        data = response.json()

        if "access_token" in data:
            access_token = data["access_token"]
            session["access_token"] = access_token

            try:
                with open(CREDENTIALS_FILE, 'w') as token_file:
                    json.dump({"access_token": access_token}, token_file)
            except Exception as e:
                return f"Error writing to {CREDENTIALS_FILE}: {e}"

            user_response = requests.get(
                f"https://graph.facebook.com/v12.0/me?fields=id,name,email&access_token={access_token}"
            )
            user_data = user_response.json()
            return redirect(url_for('home'))
        else:
            return f"Error: {data.get('error', 'Unknown error')}"
    else:
        return "Error: No code provided or invalid code"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port)

# import facebook
# import json
# from datetime import datetime, timedelta
# import time

# class FacebookManager:
#     def __init__(self):
#         self.credentials = self._load_credentials()
#         self.facebook_api = self._initialize_facebook_api()

#     def _load_credentials(self):
#         with open('facebook_token.json', 'r') as file:
#             return json.load(file)
        

#     def _initialize_facebook_api(self):
#         access_token = self.credentials['access_token']
#         print(access_token)
#         return facebook.GraphAPI(access_token)

#     def schedule_post(self, content: str, datetime_str: str):
#         post_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
#         current_time = datetime.now()

#         delay = (post_time - current_time).total_seconds()
#         if delay > 0:
#             time.sleep(delay)

#         self._post_to_facebook(content)

#     def _post_to_facebook(self, content: str):
#         try:
#             print("Posting facebook....")
#             post = self.facebook_api.put_object(parent_object='me', connection_name='feed', message=content)
#             print(post)
#         except facebook.GraphAPIError as e:
#             print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     facebook_manager = FacebookManager()
#     facebook_manager._post_to_facebook('Excited to announce our new project!')
