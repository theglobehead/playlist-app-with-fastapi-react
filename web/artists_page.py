from flask import Blueprint, render_template, session, request, redirect, url_for

from controllers.controller_database import ControllerDatabase
from models.artist import Artist

artists_view = Blueprint("artists", __name__)


@artists_view.route("/", methods=['GET'])
def artists():
    """
    View for the discover page
    :return: renders the artists view
    """
    user_id = session.get("user_id")
    user = ControllerDatabase.get_user(user_id)

    page_size = 50
    artists_list = ControllerDatabase.get_artists(page_size)

    return render_template("artists.html", artists=artists_list, user=user)


@artists_view.route("/create-artist", methods=['POST'])
def create_artist():
    artist_name = request.form.get("artist_name")
    parent_artist_name = request.form.get("parent_artist_name")
    parent_artist = ControllerDatabase.get_artist_by_name(artist_name=parent_artist_name)

    ControllerDatabase.insert_artist(artist=Artist(artist_name=artist_name), parent_artist=parent_artist)

    return redirect(url_for("artists.artists"))


@artists_view.route("/check-if-artist-exists", methods=['POST'])
def check_if_artist_exists():
    artist_name = request.form.get("artist_name", type=str)
    artist = ControllerDatabase.get_artist_by_name(artist_name)

    result = bool(artist)

    return {"result": result}
