from flask import Blueprint, render_template, session

from controllers.controller_song import ControllerSong

discover_view = Blueprint("discover", __name__)


@discover_view.route("/", methods = ['GET', 'POST'])
def discover():
    user = session.get("user")

    page_song_amount = 6
    songs = ControllerSong.get_songs(amount=page_song_amount)
    return render_template("discover_page.html", user=user, songs=songs)
