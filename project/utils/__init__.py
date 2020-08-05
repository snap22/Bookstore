# v tomto balicku bude:
#   -metoda na vygenerovanie nahodneho cisla pre objednavku
#   -

from project.models.shop import Author, Book
from project import db

def search_books(phrase):
    words = phrase.split(" ")
    found_books = None
    for word in words:
        books = Book.query.filter(Book.title.contains(word))
        if books.count() > 0:
            found_books = books
            break

    if found_books is None or found_books.count() == 0:
        author = Author.query.filter(Author.name.contains(words[0])).first()
        if author is None:
            return None
        found_books = author.books

    return found_books