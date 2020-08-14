from flask import Blueprint, session, flash, redirect, render_template, url_for, request, Markup
from project.books.utils import add_book_to_cart, remove_book_from_cart
from project.models.shop import Book, Author
from project.models.account import Info
from project.users.account.forms import ContactForm
from flask_login import current_user

shop = Blueprint("shop", __name__)

@shop.route("/cart/")
def cart():
    if "cart" in session:
        books = Book.query.filter(Book.id.in_(session["cart"])).all()
        price = round(sum(book.price for book in books), 2)
    else:
        books = None
        price = 0
    return render_template("shop/cart.html", selected_books=books, author=Author.query, full_price=price)


@shop.route("/addToCart/<int:book_id>/")
def add_to_cart(book_id):
    add_book_to_cart(book_id)
    flash(Markup(f"Kniha <b>{Book.query.get(book_id).title}</b> bola pridaná do košíka"), "info")

    return redirect(request.referrer)
        
   
@shop.route("/removeFromCart/<int:book_id>/")
def remove_from_cart(book_id):
    remove_book_from_cart(book_id)
    flash(Markup(f"Kniha <b>{Book.query.get(book_id).title}</b> bola zmazaná z košíka"), "info")

    return redirect(request.referrer)
        
   

@shop.route("/payment/", methods=["GET", "POST"])
def payment():
    if current_user.is_authenticated and Info.query.get(current_user.info_id):
        #ak je pouzivatel prihlaseny a ma vyplnene kontaktne udaje tak sa nehodi formular na kontaktne udaje
        pass
    form = ContactForm()

    return render_template("shop/payment.html", form=form)