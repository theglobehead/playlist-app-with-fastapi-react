from flask import Blueprint, render_template, session, request, redirect, url_for

from controllers.controller_playlist import ControllerPlaylist
from controllers.controller_song import ControllerSong

discover_view = Blueprint("discover", __name__)


@discover_view.route("/", methods = ['GET', 'POST'])
def discover():
    """
    View for the discover page
    :return: renders the discover view
    """
    user = session.get("user")

    page_song_amount = 6
    songs = ControllerSong.get_songs(amount=page_song_amount)
    user_playlists = ControllerPlaylist.get_user_playlists(user["id"])
    return render_template("discover_page.html", user=user, songs=songs, user_playlists=user_playlists)

@discover_view.route("/add-song", methods = ['GET', 'POST'])
def add_song():
    playlist_uuid = request.form.get("playlist_uuid")
    song_uuid = request.form.get("song_uuid")

    playlist_id = ControllerPlaylist.get_playlist_id_by_uuid(playlist_uuid)
    song_id = ControllerSong.get_song_id_by_uuid(song_uuid)

    ControllerPlaylist.add_song(playlist_id, song_id)

    return redirect(url_for("discover.discover"))
