from flask import Flask, redirect
from web.login_page import login_view
from web.register_page import register_view

app = Flask(__name__)

@app.route('/')  
def home():
    return redirect("/login")

if __name__ == "__main__":
    app.register_blueprint(login_view, url_prefix="/login")
    app.register_blueprint(register_view, url_prefix="/register")
    app.run(debug=True)