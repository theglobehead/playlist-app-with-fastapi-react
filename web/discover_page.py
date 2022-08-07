from flask import Blueprint, render_template, session, request, redirect, url_for

from controllers.controller_database import ControllerDatabase
from controllers.controller_playlist import ControllerPlaylist
from controllers.controller_song import ControllerSong

discover_view = Blueprint("discover", __name__)


@discover_view.route("/", methods = ['GET', 'POST'])
def discover():
    """
    View for the discover page
    :return: renders the discover view
    """
    user_uuid = session.get("user_uuid")
    user = ControllerDatabase.get_user_by_uuid(user_uuid)

    page_song_amount = 6
    songs = ControllerDatabase.get_songs(amount=page_song_amount)
    return render_template("discover_page.html", user=user, songs=songs, user_playlists=user.playlists)


@discover_view.route("/add-song", methods=['GET', 'POST'])
def add_song():
    playlist_uuid = request.form.get("playlist_uuid")
    song_uuid = request.form.get("song_uuid")

    playlist_id = ControllerDatabase.get_playlist_id_by_uuid(playlist_uuid)
    song_id = ControllerDatabase.get_song_id_by_uuid(song_uuid)

    ControllerDatabase.add_song_to_playlist(playlist_id, song_id)

    return redirect(url_for("discover.discover"))
