from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user
from project.models import Post

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home/")
def home():
    return render_template("main/home.html", title="Home")

@main.route("/contact/")
def contact():
    return render_template("main/contact.html", title="Home")

@main.route("/about/")
def about():
    return render_template("main/about.html", title="Home")

