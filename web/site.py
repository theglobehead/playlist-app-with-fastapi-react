from flask import Blueprint, session, redirect, url_for

from modules.controller_user import ControllerUser

site = Blueprint("site", __name__)


@site.route("/logout", methods=['GET', 'POST'])
def logout():
    session["user"] = None
    session.clear()
    return redirect(url_for("login.login"))


@site.route("/profile_picture/<uuid>", methods=['GET', 'POST'])
def get_profile_pic(uuid: str) -> str:
    result = ControllerUser.get_profile_pic(uuid)
    print(result)
    return result
