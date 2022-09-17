import logging
from datetime import datetime
from uuid import uuid4
import psycopg2.extras
from flask import Flask, redirect, session, url_for, request, render_template
from flask_babel import Babel
from loguru import logger
from requests import Session
from werkzeug.exceptions import HTTPException

from controllers.constants import LOGS_PATH
from controllers.controller_database import ControllerDatabase

from web.login_page import login_view
from web.register_page import register_view
from web.playlists_pages import playlists_view
from web.discover_page import discover_view
from web.artists_page import artists_view
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


@babel.localeselector
def get_locale() -> str:
    """
    Used for determining the language of the website
    If the locale is in the session it returns the local
    If the locale is not in the session it returns the best local according to the users browser
    :return: the locale as "lv" or "en"
    """
    locale = request.accept_languages.best_match(["lv", "en"])
    if "locale" in session:
        locale = session.get("locale")

    session["locale"] = locale
    return locale


@app.route('/')
def home():
    """
    The home view
    :return: Redirects to the login view if the user isn't logged in,
             otherwise it returns to the your_playlist view
    """
    print(request.cookies.get("token"))

    result = redirect(url_for("login.login"))
    if "user_id" in session:
        result = redirect(url_for("playlists.your_playlists"))

    return result


@app.errorhandler(Exception)
def error_page(error):
    """
    This function is called any time a fatal error occurs
    :param error: The Exception that caused the error
    :return: Renders the error page with the appropriate error code
    """
    logger.exception(error)
    error_code = 500

    if isinstance(error, HTTPException):
        error_code = error.code

    return render_template("error_page.html", error_message=f"Error: { error_code }"), error_code


@app.before_request
def check_user_in():
    """
    Before each request, it checks if the user is logged in.
    If it isn't and the user has a session token, the user gets logged in.
    :return: None
    """
    if "user_id" in session:
        return  # I know that this is bad practice, but is it maybe acceptable in this situation, to avoid indentation?

    token_uuid = request.cookies.get("token")
    if token_uuid:
        token = ControllerDatabase.get_token_by_uuid(token_uuid)
        user = ControllerDatabase.get_user(token.user_user_id)

        if user:
            session["user_id"] = user.user_id


if __name__ == "__main__":
    logger.add("./logs/{time:YYYY-MM-DD}.log", colorize=True, rotation="00:00")
    app.register_blueprint(site, url_prefix="/site")
    app.register_blueprint(login_view, url_prefix="/login")
    app.register_blueprint(register_view, url_prefix="/register")
    app.register_blueprint(playlists_view, url_prefix="/playlists")
    app.register_blueprint(discover_view, url_prefix="/discover")
    app.register_blueprint(artists_view, url_prefix="/artists")
    app.run(debug=True)
