from flask import Blueprint, redirect, url_for, render_template, session, request, flash, Markup
from flask_login import current_user
from project.models.shop import Book, Author
from project.utils import search_books, search_by_author_name
#from project.main.utils import resize_pictures
import os
from project.main.utils import get_pictures


main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home/")
def home():
    
    pictures = get_pictures()
    return render_template("main/home.html", title="Home", pictures=pictures)


@main.route("/contact/")
def contact():
    return render_template("main/contact.html", title="Home")

@main.route("/about/")
def about():
    return render_template("main/about.html", title="Home")

