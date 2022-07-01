from flask import Blueprint, render_template

register_view = Blueprint("register", __name__)

@register_view.route("/", methods = ['GET', 'POST'])
def register():
    return render_template("register_page.html")