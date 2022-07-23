from flask import Blueprint, render_template, session, redirect, url_for, request

from controllers.controller_database import ControllerDatabase
from controllers.controller_playlist import ControllerPlaylist
from controllers.controller_user import ControllerUser
from utils.flask_utils import login_required

playlists_view = Blueprint("playlists", __name__)


@playlists_view.route("/your-playlists", methods=['GET'])
@login_required
def your_playlists():
    user = session.get("user")
    playlists = ControllerPlaylist.get_user_playlists(user["id"])
    result = render_template("playlist_list.html", user=user, playlists=playlists)

    return result


@playlists_view.route("/<playlist_uuid>", methods=['GET'])
@login_required
def playlist_page(playlist_uuid):
    user = session.get("user")
    playlist = ControllerPlaylist.get_playlist_by_uuid(playlist_uuid)

    result = render_template("playlist.html", user=user, playlist=playlist)
    return result


@playlists_view.route("/save-playlist", methods=['POST'])
@login_required
def save_playlist():
    user_uuid = request.form.get("owner_user_uuid")
    user_id = ControllerUser.get_id_by_uuid(user_uuid)
    playlist_name = request.form.get("playlist_name")
    ControllerDatabase.insert_play_list(playlist_name, user_id)
    return redirect(url_for("playlists.your_playlists"))
