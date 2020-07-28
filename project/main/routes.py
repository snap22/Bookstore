from flask import Blueprint, redirect, url_for, render_template

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home/")
def home():
    return render_template("layout.html", title="Home")