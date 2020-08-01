from flask import Blueprint, redirect, render_template, url_for, flash
from flask_login import current_user
from project.models.shop import Book, Author

books = Blueprint("books", __name__)

@books.route("/book/<int:book_id>/")
def book(book_id):
    found_book = Book.query.get(book_id)
    if not found_book:
        flash("Takúto knihu nemáme", "danger")
        return redirect(url_for("main.home"))

    author = Author.query.get(found_book.author_id)
    return render_template("books/book.html", item=found_book, author=author)