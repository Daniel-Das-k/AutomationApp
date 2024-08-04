from flask import Flask, render_template, redirect, url_for, session
import os
from dotenv import load_dotenv
from flask_dance.contrib.github import make_github_blueprint, github

load_dotenv()

class GitHubOAuthApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = "SECRET KEY"

        self.github_blueprint = make_github_blueprint(
            client_id=os.environ.get('GITHUB_CLIENT_ID'),
            client_secret=os.environ.get('GITHUB_CLIENT_SECRET')
        )

        self.app.register_blueprint(self.github_blueprint, url_prefix='/github_login')
        self.setup_routes()

    def setup_routes(self):
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/logout', 'logout', self.logout)

    def index(self):
        if github.authorized:
            print(github.authorized)
            account_info = github.get('/user')
            if account_info.ok:
                print(account_info)
                account_info_json = account_info.json()
                print(account_info_json)
                return render_template("index.html", user_info=account_info_json)
        else:
            return render_template("index.html", github_uri=url_for('github.login'))

    def logout(self):
        session.clear()
        return redirect("/")

    def run(self, debug=True):
        self.app.run(debug=debug)

if __name__ == "__main__":
    github_oauth_app = GitHubOAuthApp()
    github_oauth_app.run()
