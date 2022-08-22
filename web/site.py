import os

from flask import Blueprint, session, redirect, url_for, Response, request, send_from_directory, send_file

from controllers.constants import DEFAULT_PROFILE_PICTURE_PATH, PROFILE_PICTURE_PATH, SONG_PICTURE_PATH
from controllers.controller_database import ControllerDatabase

site = Blueprint("site", __name__)


@site.route("/logout", methods=['GET'])
def logout():
    """
    Used for logging a user out.
    Clears the session
    :return: Redirects to the login view
    """
    user = ControllerDatabase.get_user(user_id=session["user_id"])

    session["user"] = None
    session["user_id"] = None
    session.clear()

    if user.token.token_uuid:
        ControllerDatabase.delete_token(user.token)

    result = redirect(url_for("login.login"))
    result.delete_cookie("token")

    return result


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
    result = ""

    user_pic_path = f"{PROFILE_PICTURE_PATH}{user_uuid}.png"
    if os.path.exists(user_pic_path):
        result = user_pic_path
    else:
        result = DEFAULT_PROFILE_PICTURE_PATH

    return send_from_directory("", result)


@site.route("/songe_picture/<song_uuid>", methods=['GET'])
def get_song_pic(song_uuid: str) -> Response:
    """
    Used for getting the image for a song
    :param song_uuid: uuid od the song
    :return: returns the image as a response
    """
    result = ""

    song_pic_path = f"{SONG_PICTURE_PATH}{song_uuid}.jpg"
    if os.path.exists(song_pic_path):
        result = song_pic_path
    else:
        result = DEFAULT_PROFILE_PICTURE_PATH

    return send_from_directory("", result)
