from flask import Flask, redirect, url_for, session, render_template
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

class GoogleOAuthApp:
    def __init__(self):
        self.app = Flask(__name__)
        print(f"Client ID: {os.getenv('GOOGLE_CLIENT_ID')}")
        print(f"Client Secret: {os.getenv('GOOGLE_CLIENT_SECRET')}")
        print(f"Secret Key: {os.getenv('GOOGLE_SECRET_KEY')}")

        self.app.secret_key = os.getenv("GOOGLE_SECRET_KEY")
        self.app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
        self.app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

        self.oauth = OAuth(self.app)
        self.google = self.oauth.register(
            name='google',
            client_id=os.getenv("GOOGLE_CLIENT_ID"),
            client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
            access_token_url='https://accounts.google.com/o/oauth2/token',
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            api_base_url='https://www.googleapis.com/oauth2/v1/',
            userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
            client_kwargs={'scope': 'email profile'},
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
        )

        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/', 'home', self.home)
        self.app.add_url_rule('/login', 'login', self.login)
        self.app.add_url_rule('/authorize', 'authorize', self.authorize)
        self.app.add_url_rule('/logout', 'logout', self.logout)

    def home(self):
        login_url = url_for('login')
        user_info = session.get('profile', None)
        if user_info:
            email = user_info.get('email', 'Unknown')
            return render_template("index.html", user_info=user_info)
        return render_template("index.html", login_url=login_url)

    def login(self):
        redirect_uri = url_for('authorize', _external=True)
        return self.google.authorize_redirect(redirect_uri)

    def authorize(self):
        token = self.google.authorize_access_token()  
        resp = self.google.get('userinfo') 
        self.user_info = resp.json()    
        session['profile'] = self.user_info  

        print(f"User info: {self.user_info}")
        
        return redirect(url_for('home'))

    def logout(self):
        for key in list(session.keys()):
            session.pop(key)
        return redirect(url_for('home'))

    def run(self, debug=True):
        self.app.run(debug=debug)

if __name__ == "__main__":
    google_oauth_app = GoogleOAuthApp()
    google_oauth_app.run()

