# from flask import Flask, redirect, request, session, url_for
# import requests
# import os
# import json

# app = Flask(__name__)
# app.secret_key = "secret"
# Fb_APP_ID = "1519269175630468"
# Fb_APP_SECRET = "e04ebcfe52882ed9a9134937547e0ba0"
# Fb_REDIRECT_URI = "https://facebook-rakb.onrender.com/facebook/callback"
# PAGE_ID = "389529784241782"  # Your Page ID

# @app.route('/')
# def home():
#     access_token = session.get("access_token")
#     page_access_token = session.get("page_access_token")
#     if access_token and page_access_token:
#         return f'''
#             User Access Token: {access_token}
#             Page Access Token: {page_access_token}
#             <form action="/facebook/post" method="post">
#                 <input type="text" name="message" placeholder="Enter message to post">
#                 <button type="submit">Post to Facebook</button>
#             </form>
#         '''
#     else:
#         return "Home Page"

# @app.route('/facebook/login')
# def facebook_login():
#     return redirect(f"https://www.facebook.com/v20.0/dialog/oauth?client_id={Fb_APP_ID}&redirect_uri={Fb_REDIRECT_URI}&scope=pages_manage_posts,pages_read_engagement")

# @app.route('/facebook/callback')
# def facebook_callback():
#     code = request.args.get("code")
#     if code:
#         response = requests.get(
#             f"https://graph.facebook.com/v20.0/oauth/access_token?client_id={Fb_APP_ID}&redirect_uri={Fb_REDIRECT_URI}&client_secret={Fb_APP_SECRET}&code={code}"
#         )
#         data = response.json()
#         if "access_token" in data:
#             user_access_token = data["access_token"]
#             session["access_token"] = user_access_token

#             # Exchange user access token for page access token
#             page_access_token_response = requests.get(
#                 f"https://graph.facebook.com/v20.0/{PAGE_ID}?fields=access_token&access_token={user_access_token}"
#             )
#             page_access_token_data = page_access_token_response.json()
#             if "access_token" in page_access_token_data:
#                 page_access_token = page_access_token_data["access_token"]
#                 session["page_access_token"] = page_access_token
#                 return redirect(url_for('home'))
#             else:
#                 error_message = page_access_token_data.get('error', {}).get('message', 'Unknown error')
#                 return f"Error fetching page access token: {error_message}"
#         else:
#             error_message = data.get('error', {}).get('message', 'Unknown error')
#             return f"Error fetching user access token: {error_message}"
#     else:
#         return "Error: No code provided or invalid code"

# @app.route('/facebook/post', methods=['POST'])
# def facebook_post():
#     page_access_token = session.get("page_access_token")
#     if not page_access_token:
#         return redirect(url_for('facebook_login'))
    
#     message = request.form.get('message')
#     if not message:
#         return "Error: No message provided"
    
#     post_url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/feed"
#     post_data = {
#         'message': message,
#         'access_token': page_access_token
#     }
    
#     response = requests.post(post_url, data=post_data)
#     result = response.json()
    
#     if 'id' in result:
#         return f"Post ID: {result['id']}"
#     else:
#         error_message = result.get('error', {}).get('message', 'Unknown error')
#         return f"Error: {error_message}"

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5002))
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
    page_access_token = session.get("page_access_token")
    if access_token and page_access_token:
        return f'''
            User Access Token: {access_token}
            Page Access Token: {page_access_token}
            <form action="/facebook/post" method="post">
                <input type="text" name="message" placeholder="Enter message to post">
                <button type="submit">Post to Facebook</button>
            </form>
        '''
    else:
        return redirect(url_for('facebook_login'))

@app.route('/facebook/login')
def facebook_login():
    return redirect(f"https://www.facebook.com/v20.0/dialog/oauth?client_id={Fb_APP_ID}&redirect_uri={Fb_REDIRECT_URI}&scope=pages_manage_posts,pages_read_engagement")

@app.route('/facebook/callback')
def facebook_callback():
    code = request.args.get("code")
    if code:
        response = requests.get(
            f"https://graph.facebook.com/v20.0/oauth/access_token?client_id={Fb_APP_ID}&redirect_uri={Fb_REDIRECT_URI}&client_secret={Fb_APP_SECRET}&code={code}"
        )
        data = response.json()
        if "access_token" in data:
            user_access_token = data["access_token"]
            session["access_token"] = user_access_token

            # Fetch the list of pages managed by the user
            pages_response = requests.get(
                f"https://graph.facebook.com/v20.0/me/accounts?access_token={user_access_token}"
            )
            pages_data = pages_response.json()
            if 'data' in pages_data:
                # Select the first page in the list (or implement logic to select a specific page)
                first_page = pages_data['data'][0]
                page_access_token = first_page['access_token']
                session["page_access_token"] = page_access_token
                session["page_id"] = first_page['id']
                return redirect(url_for('home'))
            else:
                error_message = pages_data.get('error', {}).get('message', 'Unknown error')
                return f"Error fetching pages: {error_message}"
        else:
            error_message = data.get('error', {}).get('message', 'Unknown error')
            return f"Error fetching user access token: {error_message}"
    else:
        return "Error: No code provided or invalid code"

@app.route('/facebook/post', methods=['POST'])
def facebook_post():
    page_access_token = session.get("page_access_token")
    page_id = session.get("page_id")
    if not page_access_token or not page_id:
        return redirect(url_for('facebook_login'))
    
    message = request.form.get('message')
    if not message:
        return "Error: No message provided"
    
    post_url = f"https://graph.facebook.com/v20.0/{page_id}/feed"
    post_data = {
        'message': message,
        'access_token': page_access_token
    }
    
    response = requests.post(post_url, data=post_data)
    result = response.json()
    
    if 'id' in result:
        return f"Post ID: {result['id']}"
    else:
        error_message = result.get('error', {}).get('message', 'Unknown error')
        return f"Error: {error_message}"

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
#         access_token = self.credentials['page_access_token']
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
