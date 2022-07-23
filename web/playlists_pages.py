from flask import Blueprint, render_template, session

from controllers.controller_playlist import ControllerPlaylist
from utils.flask_utils import login_required

playlists_view = Blueprint("playlists", __name__)


@playlists_view.route("/your-playlists", methods=['GET', 'POST'])
@login_required
def your_playlists():
    user = session.get("user")
    playlists = ControllerPlaylist.get_user_playlists(user["id"])
    result = render_template("playlist_list.html", user=user, playlists=playlists)

    return result


@playlists_view.route("/<playlist_uuid>", methods=['GET', 'POST'])
@login_required
def playlist_page(playlist_uuid):
    user = session.get("user")
    playlist = ControllerPlaylist.get_playlist_by_uuid(playlist_uuid)

    result = render_template("playlist.html", user=user, playlist=playlist)
    return result
