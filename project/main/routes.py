from flask import Blueprint, redirect, url_for, render_template, session, request, flash
from flask_login import current_user
from project.models.shop import Book, Author



main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home/")
def home():
    page = request.args.get("page", 1, type=int)
    books = Book.query.paginate(page=page, per_page=5)

    authors = Author.query
    return render_template("main/home.html", title="Home", books=books, authors=authors)


@main.route("/contact/")
def contact():
    return render_template("main/contact.html", title="Home")

@main.route("/about/")
def about():
    return render_template("main/about.html", title="Home")

@main.route("/search/")
def search():
    page = request.args.get("page", 1, type=int)
    search_obj = request.args.get("q")
    if search_obj:
        flash(search_obj, "primary")
        first_word = search_obj.split(" ")[0]
        books = Book.query.filter_by(title=search_obj).paginate(page=page, per_page=5)
    else:
        books = Book.query.paginate(page=page, per_page=5)

    authors = Author.query
    return render_template("main/home.html", title="Home", books=books, authors=authors)

