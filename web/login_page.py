from flask import Blueprint, render_template

login_view = Blueprint("login", __name__)

@login_view.route("/", methods = ['GET', 'POST'])
def login():
    return render_template("login_page.html")