from flask import Flask, render_template, request, redirect, url_for, make_response
from sqla_wrapper import SQLAlchemy

db = SQLAlchemy("sqlite:///db.sqlite")

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False)
    email = db.Column(db.String, unique=False)

db.create_all()

app = Flask(__name__)

@app.route("/")
def index():
    email = request.cookies.get("email")
    if email:
        user = db.query(User).filter_by(email=email).first()
    else:
        user = None

    return render_template("index.html", user=user)

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("name")
    email = request.form.get("email")

    user = User(name=name, email=email)

    db.add(user)
    db.commit()

    response = make_response(redirect(url_for("index")))
    response.set_cookie("email", email)

    return response

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)