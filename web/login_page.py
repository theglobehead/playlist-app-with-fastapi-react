import flask
from flask import Blueprint, render_template, request, session, redirect, url_for

from controllers.controller_user import ControllerUser

login_view = Blueprint("login", __name__)


@login_view.route("/", methods=['GET', 'POST'])
def login():
    result = render_template("login_page.html")

    if request.method == "POST":
        form = request.form
        name = form.get("username").strip()
        password = form.get("password").strip()

        user = ControllerUser.authenticate_user(name, password)

        if user:
            session["user"] = user
            result = redirect(url_for("your-playlists.your_playlists"))
        else:
            flask.flash("Incorrect login details!")

    return result
