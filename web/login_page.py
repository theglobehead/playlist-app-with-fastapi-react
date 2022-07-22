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

        username_exists = ControllerUser.check_if_username_taken(name)
        password_matches = False

        if username_exists:
            user_id = ControllerUser.get_id_by_name(name)
            user = ControllerUser.get_user(user_id)
            hashed_password = ControllerUser.hash_password(password, user.password_salt)

            if user.hashed_password == hashed_password:
                password_matches = True
                session["user"] = user
                result = redirect(url_for("your-playlists.your_playlists"))

        if not username_exists or not password_matches:
            flask.flash("Incorrect login details!")

    return result
