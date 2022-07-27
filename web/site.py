from flask import Blueprint, session, redirect, url_for

from controllers.controller_song import ControllerSong
from controllers.controller_user import ControllerUser

site = Blueprint("site", __name__)


@site.route("/logout", methods=['GET', 'POST'])
def logout():
    session["user"] = None
    session.clear()
    return redirect(url_for("login.login"))


@site.route("/profile_picture/<user_uuid>", methods=['GET', 'POST'])
def get_profile_pic(user_uuid: str) -> str:
    result = ControllerUser.get_profile_pic(user_uuid)
    return result


@site.route("/songe_picture/<song_uuid>", methods=['GET', 'POST'])
def get_song_pic(song_uuid: str) -> str:
    result = ControllerSong.get_song_pic(song_uuid)
    return result


