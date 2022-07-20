from flask import Blueprint, render_template, session

your_playlists_view = Blueprint("your-playlists", __name__)


@your_playlists_view.route("/", methods=['GET', 'POST'])
def your_playlists():
    user = session["user"]
    result = render_template("playlist_list.html", user=user)

    return result
