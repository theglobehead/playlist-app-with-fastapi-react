from flask import Blueprint, session, redirect, url_for, Response, request

from controllers.controller_database import ControllerDatabase
from controllers.controller_song import ControllerSong
from controllers.controller_user import ControllerUser

site = Blueprint("site", __name__)


@site.route("/logout", methods=['GET'])
def logout():
    """
    Used for logging a user out.
    Clears the session
    :return: Redirects to the login view
    """
    session["user"] = None
    session["user_uuid"] = None
    session.clear()
    return redirect(url_for("login.login"))


@site.route("/change_locale/<locale>", methods=['GET'])
def change_locale(locale: str):
    """
    Used for changing a users' locale
    :return: Redirects to the page from which this function was called
    """
    session["locale"] = locale
    return redirect(request.referrer)


@site.route("/profile_picture/<user_uuid>", methods=['GET'])
def get_profile_pic(user_uuid: str) -> Response:
    """
    Used for getting the profile picture of a user
    :param user_uuid: uuid od the song
    :return: returns the image as a response
    """
    result = ControllerDatabase.get_user_profile_pic(user_uuid)
    return result


@site.route("/songe_picture/<song_uuid>", methods=['GET'])
def get_song_pic(song_uuid: str) -> Response:
    """
    Used for getting the image for a song
    :param song_uuid: uuid od the song
    :return: returns the image as a response
    """
    result = ControllerDatabase.get_song_pic(song_uuid)
    return result
