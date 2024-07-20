import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["FACEBOOK_OAUTH_CLIENT_ID"] = os.environ.get("FACEBOOK_OAUTH_CLIENT_ID")
app.config["FACEBOOK_OAUTH_CLIENT_SECRET"] = os.environ.get("FACEBOOK_OAUTH_CLIENT_SECRET")
app.config["FACEBOOK_OAUTH_REDIRECT_URI"] = "https://facebook-rakb.onrender.com"
facebook_bp = make_facebook_blueprint(
    client_id=app.config["FACEBOOK_OAUTH_CLIENT_ID"],
    client_secret=app.config["FACEBOOK_OAUTH_CLIENT_SECRET"],
    redirect_to="facebook.login"
)
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
