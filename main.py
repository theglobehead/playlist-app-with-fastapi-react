import psycopg2.extras
from flask import Flask, redirect, session, url_for

from web.login_page import login_view
from web.register_page import register_view
from web.your_playlists_page import your_playlists_view
from web.site import site

app = Flask(__name__)
app.config['SECRET_KEY'] = "8f42a73054b1749h8f58848be5e6502c"

psycopg2.extras.register_uuid()


@app.route('/')
def home():
    result = redirect(url_for("login.login"))
    if "user" in session:
        result = redirect(url_for("your-playlists.your_playlists"))

    return result


if __name__ == "__main__":
    app.register_blueprint(site, url_prefix="/site")
    app.register_blueprint(login_view, url_prefix="/login")
    app.register_blueprint(register_view, url_prefix="/register")
    app.register_blueprint(your_playlists_view, url_prefix="/your-playlists")
    app.run(debug=True)
