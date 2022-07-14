import flask
from flask import Blueprint, render_template, request

from modules.controller_database import ControllerDatabase
from modules.controller_user import ControllerUser

register_view = Blueprint("register", __name__)

@register_view.route("/", methods = ['GET', 'POST'])
def register():
    if request.method == "POST":
        form = request.form
        name = form.get("username")
        password1 = form.get("password1")
        password2 = form.get("password2")

        form_is_valid = validate_form(name=name, pass1=password1, pass2=password2)

        if form_is_valid:
            ControllerDatabase.insert_user(name=name, password=password1)

        return render_template("login_page.html")

    return render_template("register_page.html")


def validate_form(name: str, pass1: str, pass2: str):
    if not all((pass1, pass2)):
        flask.flash("Both passwords must be entered!")
        return False

    if pass1 != pass2:
        flask.flash("Passwords are not equal!")
        return False

    if ControllerUser.check_if_username_taken(name=name):
        flask.flash("Username is already taken!")
        return False

    return True
