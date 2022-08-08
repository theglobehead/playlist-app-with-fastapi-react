import psycopg2.extras
from flask import Flask, redirect, session, url_for, request
from flask_babel import Babel
from requests import Session

from web.login_page import login_view
from web.register_page import register_view
from web.playlists_pages import playlists_view
from web.discover_page import discover_view
from web.site import site

app = Flask(__name__)
app.config["SECRET_KEY"] = "8f42a73054b1749h8f58848be5e6502c"
app.config["BABEL_DEFAULT_LOCALE"] = "en"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["UPLOAD_FOLDER"] = "/static/uploads/"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

babel = Babel(app)

psycopg2.extras.register_uuid()


@app.route('/')
def home():
    """
    The home view
    :return: Redirects to the login view if the user isn't logged in,
             otherwise it returns to the your_playlist view
    """
    result = redirect(url_for("login.login"))
    if "user_uuid" in session:
        result = redirect(url_for("playlists.your_playlists"))

    return result


if __name__ == "__main__":
    app.register_blueprint(site, url_prefix="/site")
    app.register_blueprint(login_view, url_prefix="/login")
    app.register_blueprint(register_view, url_prefix="/register")
    app.register_blueprint(playlists_view, url_prefix="/playlists")
    app.register_blueprint(discover_view, url_prefix="/discover")
    app.run(debug=True)
