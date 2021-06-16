from flask import Blueprint, redirect, url_for, render_template
from flask_admin import BaseView, expose
from flask_security import login_required, current_user

from ..models.models import User

home = Blueprint("home", __name__)


@home.route("/")
@login_required
def home_page():
    if current_user.is_authenticated:
        return redirect(url_for("home.dashboard", name=current_user.email))
    return redirect(url_for("security.login"))


@home.route("/dashboard/<name>")
def dashboard(name):
    return render_template("home.html", name=name)
    # return f"Welcome %s, We also have these users: <h2>{User.query.all()}</h2>" % name


def find_user(email):
    return User.query.filter_by(email=email).first()


class HomePageFromAdmin(BaseView):

    @expose('/')
    def index(self):
        return redirect(url_for('home.home_page'))
