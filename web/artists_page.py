from flask import Blueprint, render_template, session, request, redirect, url_for

from controllers.controller_database import ControllerDatabase

artists_view = Blueprint("artists", __name__)


@artists_view.route("/", methods=['GET'])
def artists():
    """
    View for the discover page
    :return: renders the discover view
    """
    user_id = session.get("user_id")
    user = ControllerDatabase.get_user(user_id)

    page_size = 10
    artists_list = ControllerDatabase.get_artists(page_size)

    return render_template("artists.html", artists=artists_list, user=user)
