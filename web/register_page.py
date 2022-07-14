from flask import Blueprint, render_template, request

from modules.controller_database import ControllerDatabase

register_view = Blueprint("register", __name__)

@register_view.route("/", methods = ['GET', 'POST'])
def register():
    if request.method == "POST":
        form = request.form
        name = form.get("username")
        password1 = form.get("password1")

        ControllerDatabase.insert_user(name=name, password=password1)

        return render_template("login_page.html")

    return render_template("register_page.html")
