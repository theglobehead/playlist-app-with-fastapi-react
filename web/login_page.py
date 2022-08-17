import datetime

import flask
from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_babel import gettext

from controllers.controller_database import ControllerDatabase
from controllers.controller_user import ControllerUser
from models.user import User

login_view = Blueprint("login", __name__)


@login_view.route("/", methods=['GET', 'POST'])
def login():
    """
    View for the login page.
    if the method is POST and the form data is valid, it logs the user in
    :return: renders the login view or redirects to the your_playlists view
    """
    result = render_template("login_page.html")

    if request.method == "POST":
        form = request.form
        name = form.get("username").strip()
        password = form.get("password").strip()
        remember_me = form.get("remember_me")

        user = ControllerUser.authenticate_user(name, password, remember_me)

        if user:
            session["user_uuid"] = user.user_uuid
            result = redirect(url_for("playlists.your_playlists"))
            result.set_cookie("token", user.token.token_uuid, expires=datetime.datetime.now() + datetime.timedelta(days=30))
        else:
            flask.flash(gettext("error_msg.incorrect_login_details"))

    return result
