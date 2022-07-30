import http

from flask import Blueprint, render_template, session, redirect, url_for, request

from controllers.controller_database import ControllerDatabase
from controllers.controller_playlist import ControllerPlaylist
from controllers.controller_song import ControllerSong
from controllers.controller_user import ControllerUser
from utils.flask_utils import login_required

playlists_view = Blueprint("playlists", __name__)


@playlists_view.route("/your-playlists", methods=['GET'])
@login_required
def your_playlists():
    """
    View for user playlists
    :return: renders the view for your_playlists.html
    """
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    user_uuid = session.get("user_uuid")
    user = ControllerDatabase.get_user_by_uuid(user_uuid)
    print("user:", user)
    playlists = ControllerDatabase.get_user_playlists(user)
    result = render_template("your_playlists.html", user=user, playlists=playlists)

    return result


@playlists_view.route("/<playlist_uuid>", methods=['GET'])
@login_required
def playlist_page(playlist_uuid):
    """
    View for a playlist
    :param playlist_uuid: uuid of the playlist that needs to be displayed
    :return: renders the view for playlist.html
    """
    user_uuid = session.get("user_uuid")
    user = ControllerDatabase.get_user_by_uuid(user_uuid)

    playlist = ControllerDatabase.get_playlist_by_uuid(playlist_uuid)

    result = render_template("playlist.html", user=user, playlist=playlist)
    return result


@playlists_view.route("/save-playlist", methods=['POST'])
@login_required
def save_playlist():
    """
    Used for saving a playlist
    Gets the uuid of the user and the name of the playlist from a from
    :return: Redirects to the playlist_list view
    """
    user_uuid = request.form.get("owner_user_uuid")
    user_id = ControllerDatabase.get_user_by_uuid(user_uuid)
    playlist_name = request.form.get("playlist_name")
    ControllerDatabase.insert_playlist(playlist_name, user_id)
    return redirect(url_for("playlists.your_playlists"))

@playlists_view.route("/delete-playlist/<playlist_uuid>", methods=['GET'])
@login_required
def delete_playlist(playlist_uuid: str):
    """
    Used for deleting a playlist from the playlist view
    :param playlist_uuid: The uuid of the playlist that should be deleted
    :return: Redirects to the playlist_list view
    """
    playlist_id = ControllerDatabase.get_playlist_id_by_uuid(playlist_uuid)
    ControllerDatabase.delete_playlist(playlist_id)
    return redirect(url_for("playlists.your_playlists"))

@playlists_view.route("/remove-song", methods=['GET', 'POST'])
@login_required
def remove_song():
    """
    Ajax endpoint for deleting a song from a playlist
    :return: http status no content
    """
    playlist_uuid = request.form.get("playlist_uuid")
    song_uuid = request.form.get("song_uuid")

    song_id = ControllerDatabase.get_song_id_by_uuid(song_uuid)
    playlist_id = ControllerDatabase.get_playlist_id_by_uuid(playlist_uuid)

    ControllerDatabase.remove_song_from_playlist(playlist_id, song_id)

    return "", http.HTTPStatus.NO_CONTENT
