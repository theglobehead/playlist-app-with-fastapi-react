import flask
from flask import Blueprint, render_template, request, redirect, url_for
from flask_babel import gettext
from loguru import logger

from controllers.controller_database import ControllerDatabase
from controllers.controller_user import ControllerUser


register_view = Blueprint("register", __name__)

@register_view.route("/", methods = ['GET', 'POST'])
def register():
    """
    View for the register page.
    If the method is POST and the form data is correct. It registers a new user
    :return: Renders the register view or redirects to the login view
    """
    result = render_template("register_page.html")

    if request.method == "POST":
        form = request.form
        name = form.get("username").strip()
        password1 = form.get("password1").strip()
        password2 = form.get("password2").strip()

        form_is_valid = validate_form(name=name, pass1=password1, pass2=password2)

        if form_is_valid:
            try:
                ControllerUser.create_user(name=name, password=password1)
                result = redirect(url_for("login.login"))
            except Exception as e:
                flask.flash(gettext("error_msg.something_went_wrong"))
                logger.exception(e)

    return result


def validate_form(name: str, pass1: str, pass2: str):
    """
    Used for validating a register form.
    If the form is invalid, it flashes a message.
    :param name: the username entered
    :param pass1: the first password entered
    :param pass2: the second password entered
    :return: boolean of weather or not the form is valid
    """
    result = True

    if not all((pass1, pass2)):
        flask.flash(gettext("error_msg.enter_both_passwords"))
        result = False
    elif not name:
        flask.flash(gettext("error_msg.no_username_entered"))
        result = False
    elif len(name) > 64:
        flask.flash(gettext("error_msg.username_too_long"))
        result = False
    elif pass1 != pass2:
        flask.flash(gettext("error_msg.password_too_short"))
        result = False
    elif len(pass1) < 8:
        flask.flash(gettext("error_msg.passwords_must_be_equal"))
        result = False
    elif ControllerDatabase.check_if_username_taken(name=name):
        flask.flash(gettext("error_msg.username_taken"))
        result = False

    return result
