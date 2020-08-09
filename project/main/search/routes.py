from flask import Blueprint, redirect, render_template, request, flash, url_for, Markup
from project.models.shop import Book, Author
from project.utils import search_books, search_by_author_name

book_search = Blueprint("search", __name__)

@book_search.route("/search/")
def search():
    page = request.args.get("page", 1, type=int)
    search_obj = request.args.get("q")
    if search_obj:
        flash(Markup(f"Hľadanie výrazu <b> {search_obj} </b>"), "info")
        #fail
        found_books = search_books(search_obj)
        
        if found_books is None:
            flash("Nenašli sa žiadne knihy pre zadaný výraz", "warning")
            return redirect(url_for("search.search_all"))
            

        books = found_books.paginate(page=page, per_page=5)
    else:
        return redirect(url_for("main.home", page=page))

    authors = Author.query
    return render_template("main/searchBooks.html", title="Home", books=books, authors=authors)


@book_search.route("/search/all/")
def search_all():
    page = request.args.get("page", 1, type=int)

    books = Book.query.paginate(page=page, per_page=5)
    authors = Author.query
    return render_template("main/searchBooks.html", title="Home", books=books, authors=authors)



@book_search.route("/search/author/")
def search_by_author():
    author_name = request.args.get("author_name")
    page = request.args.get("page", 1, type=int)
    found_books = search_by_author_name(author_name).paginate(page=page, per_page=5)
    if found_books is None:
        
        flash("Nemáme žiadne knihy od tohto autora", "warning")
        return redirect(url_for("main.home"))
        
    else:
        flash(Markup(f"Knihy od <b>{author_name}</b>"), "info")

    return render_template("main/searchBooks.html", books=found_books, authors=Author.query)
