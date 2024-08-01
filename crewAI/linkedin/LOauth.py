import webbrowser
from flask import Flask, request, redirect, session, url_for
import requests
from dotenv import load_dotenv
load_dotenv()
import os
import threading 

CLIENT_ID=os.getenv('LINKEDIN_CLIENT_ID')
REDIRECT_URI=os.getenv('LINKEDIN_REDIRECT_URI')
CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
app = Flask(__name__)
app.secret_key = '1234'  

@app.route('/')
def home():
    return 'Welcome to the LinkedIn OAuth demo! <a href="/linkedin/login">Login with LinkedIn</a>'

@app.route('/linkedin/login')
def linkedin_login():
    session.clear()
    authorization_url = 'https://www.linkedin.com/oauth/v2/authorization'
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': 'openid+profile+email+w_member_social'
    }
    url = f"{authorization_url}?response_type={params['response_type']}&client_id={params['client_id']}&redirect_uri={params['redirect_uri']}&scope={params['scope']}"
    print(url)
    return redirect(url)

@app.route('/linkedin/callback')
def linkedin_callback():
    code = request.args.get('code')
    if code:
        user=str(input("Enter user name :"))
        access_token = get_access_token(code)
        print(acc)
        session['access_token'] = access_token
        uid=get_id(access_token)
        with open("details", "w") as f:
            f.write(f"access_token({user})={access_token}\n")
            f.write(f"id({user})={uid}\n")
       
        return 'LinkedIn OAuth successful!'
    else:
        return 'LinkedIn OAuth failed!'

def get_id(access_token):
    url = 'https://api.linkedin.com/v2/userinfo'
    headers = {
                'Authorization': f'Bearer {access_token}'
            }
    print(headers)
    response = requests.get(url, headers=headers)
    return response.json().get('sub')
    
    
    
def get_access_token(code):
    access_token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(access_token_url, data=data)
    print(response.json().get('access_token'))
    return response.json().get('access_token')

def open_browser():
    webbrowser.open('http://127.0.0.1:5000/linkedin/login')
if __name__ == '__main__':
    open_browser()
    app.run(debug=True)