from flask import Blueprint, redirect, url_for, render_template, session, request, flash, Markup
from flask_login import current_user
from project.models.shop import Book, Author
from project.utils import search_books


main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home/")
def home():
    page = request.args.get("page", 1, type=int)
    books = Book.query.order_by(Book.id.desc()).paginate(page=page, per_page=5)

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
        flash(Markup(f"Hľadanie výrazu <b> {search_obj} </b>"), "info")
        #fail
        found_books = search_books(search_obj)
        
        if found_books is None:
            flash("Nenašli sa žiadne knihy pre zadaný výraz", "warning")
            return redirect(url_for("main.home"))

        books = found_books.paginate(page=page, per_page=5)
    else:
        return redirect(url_for("main.home", page=page))

    authors = Author.query
    return render_template("main/home.html", title="Home", books=books, authors=authors)

@main.route("/test/")
def test():
    return f"The test is: {x}"