from flask import Blueprint, render_template, request, redirect, url_for

login = Blueprint("login", __name__)


@login.route("/login", methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        return redirect(url_for("dashboard", name=email))
    return render_template("login.html")
