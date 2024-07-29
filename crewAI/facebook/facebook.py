
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
#     print(access_token)
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
#     port = int(os.environ.get("PORT", 5002))
#     app.run(host='0.0.0.0', port=port)

# from flask import Flask, redirect, request, session, url_for
# import requests
# import os
# import json

# app = Flask(__name__)
# app.secret_key = "secret"
# Fb_APP_ID = "1519269175630468"
# Fb_APP_SECRET = "e04ebcfe52882ed9a9134937547e0ba0"
# Fb_REDIRECT_URI = "https://facebook-rakb.onrender.com/facebook/callback"
# PAGE_ID = "122098750820430887"  # Your Page ID

# @app.route('/')
# def home():  
#     access_token = session.get("access_token")
#     print(access_token)
#     if access_token:
#         return '''
#             Access Token: {access_token}
#             <form action="/facebook/post" method="post">
#                 <input type="text" name="message" placeholder="Enter message to post">
#                 <button type="submit">Post to Facebook</button>
#             </form>
#         '''.format(access_token=access_token)
#     else:
#         return "Home Page"

# @app.route('/facebook/login')
# def facebook_login():
#     print("Facebook login route accessed")
#     return redirect(f"https://www.facebook.com/v20.0/dialog/oauth?client_id={Fb_APP_ID}&redirect_uri={Fb_REDIRECT_URI}&scope=pages_manage_posts,pages_read_engagement,instagram_content_publish")

# @app.route('/facebook/callback')
# def facebook_callback():
#     print("Facebook callback route accessed")
#     code = request.args.get("code")
#     if code:
#         response = requests.get(
#             f"https://graph.facebook.com/v20.0/oauth/access_token?client_id={Fb_APP_ID}&redirect_uri={Fb_REDIRECT_URI}&client_secret={Fb_APP_SECRET}&code={code}"
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
#                 f"https://graph.facebook.com/v20.0/me?fields=id,name,email&access_token={access_token}"
#             )
#             print("User response:", user_response.json())
#             return redirect(url_for('home'))
#     else:
#         return "Error: No code provided or invalid code"

# @app.route('/facebook/post', methods=['POST'])
# def facebook_post():
#     access_token = session.get("access_token")
#     if not access_token:
#         return redirect(url_for('facebook_login'))
    
#     message = request.form.get('message')
#     if not message:
#         return "Error: No message provided"
    
#     post_url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/feed"
#     post_data = {
#         'message': message,
#         'access_token': access_token
#     }
    
#     response = requests.post(post_url, data=post_data)
#     result = response.json()
#     print("Post response:", result)
    
#     if 'id' in result:
#         return f"Post ID: {result['id']}"
#     else:
#         return f"Error: {result.get('error', 'Unknown error')}"

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5002))
#     app.run(host='0.0.0.0', port=port)

from flask import Flask, redirect, request, session, url_for
import requests
import json

app = Flask(__name__)
app.secret_key = "secret"
Fb_APP_ID = "1519269175630468"
Fb_APP_SECRET = "e04ebcfe52882ed9a9134937547e0ba0"
Fb_REDIRECT_URI = "https://facebook-rakb.onrender.com/facebook/callback"
PAGE_ID = "122098750820430887"

# File to save the access token
CREDENTIALS_FILE = 'Facebook_access_token.json'

@app.route('/')
def home():
    page_access_token = session.get("access_token")
    if page_access_token:
        return '''
            Access Token: {page_access_token}
            <form action="/facebook/post" method="post">
                <input type="text" name="message" placeholder="Enter message to post">
                <button type="submit">Post to Facebook</button>
            </form>
        '''.format(page_access_token=page_access_token)
    else:
        return '<a href="/facebook/login">Login with Facebook</a>'

@app.route('/facebook/login')
def facebook_login():
    print("Facebook login route accessed")
    return redirect(f"https://www.facebook.com/v20.0/dialog/oauth?client_id={Fb_APP_ID}&redirect_uri={Fb_REDIRECT_URI}&scope=pages_manage_posts,pages_read_engagement,instagram_content_publish")

@app.route('/facebook/callback')
def facebook_callback():
    code = request.args.get('code')
    if not code:
        return "Error: Missing code parameter in the callback URL."

    print("Callback route accessed with code:", code)
    token_url = f"https://graph.facebook.com/v20.0/oauth/access_token?client_id={Fb_APP_ID}&redirect_uri={Fb_REDIRECT_URI}&client_secret={Fb_APP_SECRET}&code={code}"
    response = requests.get(token_url)
    data = response.json()
    
    if 'error' in data:
        return f"Error fetching access token: {data['error']['message']}"

    access_token = data.get('access_token')
    print("Access token received:", access_token)
    
    # Save access token in session and JSON file
    session['access_token'] = access_token
    save_access_token(access_token)
    
    return redirect(url_for('home'))

def save_access_token(access_token):
    with open(CREDENTIALS_FILE, 'w') as file:
        json.dump({"access_token": access_token}, file)

@app.route('/facebook/post', methods=['POST'])
def facebook_post():
    message = request.form['message']
    page_access_token = session.get("access_token")
    if page_access_token:
        post_url = f"https://graph.facebook.com/{PAGE_ID}/feed"
        payload = {
            "message": message,
            "access_token": page_access_token
        }
        response = requests.post(post_url, data=payload)
        return f"Post Status: {response.status_code}, Response: {response.json()}"
    else:
        return redirect(url_for('facebook_login'))

if __name__ == "__main__":
    app.run(debug=True)
