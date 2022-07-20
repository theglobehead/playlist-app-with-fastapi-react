from flask import Blueprint, render_template

your_playlists_view = Blueprint("your-playlists", __name__)


@your_playlists_view.route("/", methods=['GET', 'POST'])
def your_playlists():
    result = render_template("playlist_list.html")

    return result
