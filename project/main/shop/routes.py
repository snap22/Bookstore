from flask import Blueprint, session, flash, redirect, render_template, url_for, request, Markup
from project.books.utils import add_book_to_cart, remove_book_from_cart, clear_cart
from project.models.shop import Book, Author, Order, transactions
from project.models.account import Info
from project.users.account.forms import ContactForm
from project.main.shop.forms import PaymentForm
from flask_login import current_user
from project import db

shop = Blueprint("shop", __name__)

@shop.route("/cart/")
def cart():
    if "cart" in session:
        books = Book.query.filter(Book.id.in_(session["cart"])).all()
        price = round(sum(book.price for book in books), 2)
        session["order_price"] = price
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
        
   
#really ugly shit
@shop.route("/payment/", methods=["GET", "POST"])
def payment():
    if not ("cart" in session):
        flash("Váš košík je momentálne prázdny", "danger")
        return redirect(url_for("main.home"))

    books = enumerate(Book.query.filter(Book.id.in_(session["cart"])).all())

    price = session.get("order_price")
    form = PaymentForm()
    info = None
    user_id = None 
    is_user = current_user.is_authenticated
    if is_user:
        info = Info.query.get(current_user.info_id)
        user_id = current_user.id

    if request.method == "POST":
        if form.validate_on_submit():
            new_info = Info(
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                phone_number = form.phone_number.data,
                street = form.street.data,
                city = form.city.data,
                psc = form.psc.data,
                house_number = form.house_number.data,
                state = "Slovakia",
            )

            found_duplicate = Info.query.filter_by(
                first_name=new_info.first_name,
                last_name=new_info.last_name,
                phone_number=new_info.phone_number,
                street=new_info.street,
                city=new_info.city,
                psc=new_info.psc,
                house_number=new_info.house_number
            ).first()

            if not found_duplicate:
                db.session.add(new_info)
                db.session.commit()
            else:
                new_info = found_duplicate

            if not info and is_user:     #ak je zaroven prihlaseny ale nema ulozene kontaktne udaje tak sa to ulozi
                current_user.info_id = new_info.id
                db.session.commit() 
            

            the_price = price + float(form.delivery_type.data) + float(form.pay_type.data)
            new_order = Order(buyer_id=user_id, info_id=new_info.id, total_price=the_price)
            for _, found_book in books:
                new_order.books.append(found_book)

            db.session.add(new_order)
            db.session.commit()
            clear_cart()
            #pošle sa mail
            flash("Objednávka bola úspšne vybavená. Podrobnosti boli odoslané na Váš email.", "success")
            return redirect(url_for("main.home"))
        else:
            flash("Skontrolujte si či ste si zvolili typ platby a doručenia", "info")
            
    else:
        if info:
            info = Info.query.get(current_user.info_id)
            form.first_name.data = info.first_name
            form.last_name.data = info.last_name
            form.phone_number.data =info.phone_number
            form.city.data =info.city
            form.psc.data = info.psc
            form.house_number.data = info.house_number
            form.street.data = info.street

    return render_template("shop/payment.html", form=form, price=price, books=books, authors=Author.query)