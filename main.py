from flask import Flask, redirect, render_template

app = Flask(__name__)

@app.route('/')  
def home():
    return redirect("/login")

@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template("login_page.html")

@app.route('/register')
def register():
    return render_template("register_page.html")

if __name__ == "__main__":
    app.run(debug=True)