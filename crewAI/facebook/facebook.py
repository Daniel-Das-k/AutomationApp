
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
import os
import json

app = Flask(__name__)
app.secret_key = "secret"
Fb_APP_ID = "1519269175630468"
Fb_APP_SECRET = "e04ebcfe52882ed9a9134937547e0ba0"
Fb_REDIRECT_URI = "https://facebook-rakb.onrender.com/facebook/callback"
PAGE_ID = "122098750820430887"  # Your Page ID

@app.route('/')
def home():  
    page_access_token = session.get("page_access_token")
    if page_access_token:
        return '''
            Access Token: {page_access_token}
            <form action="/facebook/post" method="post">
                <input type="text" name="message" placeholder="Enter message to post">
                <button type="submit">Post to Facebook</button>
            </form>
        '''.format(page_access_token=page_access_token)
    else:
        return "Home Page"

@app.route('/facebook/login')
def facebook_login():
    print("Facebook login route accessed")
    return redirect(f"https://www.facebook.com/v20.0/dialog/oauth?client_id={Fb_APP_ID}&redirect_uri={Fb_REDIRECT_URI}&scope=pages_manage_posts,pages_read_engagement,instagram_content_publish")

@app.route('/facebook/callback')
def facebook_callback():
    print("Facebook callback route accessed")
    code = request.args.get("code")
    if code:
        response = requests.get(
            f"https://graph.facebook.com/v20.0/oauth/access_token?client_id={Fb_APP_ID}&redirect_uri={Fb_REDIRECT_URI}&client_secret={Fb_APP_SECRET}&code={code}"
        )
        data = response.json()
        print("Response from Facebook:", data)
        if "access_token" in data:
            user_access_token = data["access_token"]
            session["access_token"] = user_access_token
            print("User access token obtained:", user_access_token)

            try:
                with open('access_token.json', 'w') as token_file:
                    json.dump({"access_token": user_access_token}, token_file)
                print("User access token saved to access_token.json")
            except Exception as e:
                print("Error writing to access_token.json:", e)

            # Exchange user access token for page access token
            page_access_token_response = requests.get(
                f"https://graph.facebook.com/v20.0/{PAGE_ID}?fields=access_token&access_token={user_access_token}"
            )
            page_access_token_data = page_access_token_response.json()
            print("Page access token response:", page_access_token_data)

            if "access_token" in page_access_token_data:
                page_access_token = page_access_token_data["access_token"]
                session["page_access_token"] = page_access_token
                print("Page access token obtained:", page_access_token)

            user_response = requests.get(
                f"https://graph.facebook.com/v20.0/me?fields=id,name,email&access_token={user_access_token}"
            )
            print("User response:", user_response.json())
            return redirect(url_for('home'))
    else:
        return "Error: No code provided or invalid code"

@app.route('/facebook/post', methods=['POST'])
def facebook_post():
    page_access_token = session.get("page_access_token")
    if not page_access_token:
        return redirect(url_for('facebook_login'))
    
    message = request.form.get('message')
    if not message:
        return "Error: No message provided"
    
    post_url = f"https://graph.facebook.com/v20.0/{PAGE_ID}/feed"
    post_data = {
        'message': message,
        'access_token': page_access_token
    }
    
    response = requests.post(post_url, data=post_data)
    result = response.json()
    print("Post response:", result)
    
    if 'id' in result:
        return f"Post ID: {result['id']}"
    else:
        return f"Error: {result.get('error', 'Unknown error')}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5002))
    app.run(host='0.0.0.0', port=port)
