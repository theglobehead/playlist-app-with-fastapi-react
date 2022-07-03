from flask import Blueprint, render_template, request
import psycopg2

register_view = Blueprint("register", __name__)

@register_view.route("/", methods = ['GET', 'POST'])
def register():
    if request.method == "POST":
        pass

    return render_template("register_page.html")