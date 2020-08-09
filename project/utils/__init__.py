# v tomto balicku bude:
#   -metoda na vygenerovanie nahodneho cisla pre objednavku
#   -

from project.models.shop import Author, Book
from project import db

class Searcher:
    def search(self, phrase):
        self.phrase = phrase


def search_books(phrase):
    words = phrase.split(" ")
    found_books = None
    for word in words:
        books = Book.query.filter(Book.title.contains(word))
        if books.count() > 0:
            found_books = books
            break

    if found_books is None or found_books.count() == 0:
        found_books = search_by_author_name(words[0])

    return found_books

def search_by_author_name(author_name):
    author = Author.query.filter(Author.name.contains(author_name)).first()
    if author:
        return author.books
    else:
        return None
