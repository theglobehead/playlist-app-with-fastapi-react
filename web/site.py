from flask import Blueprint, session, redirect

site = Blueprint("site", __name__)


@site.route("/logout", methods=['GET', 'POST'])
def logout():
    session["user"] = None
    session.clear()
    return redirect("/")
