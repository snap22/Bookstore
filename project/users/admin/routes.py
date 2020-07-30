from flask import Blueprint, url_for, render_template, redirect, flash, session, abort, Markup
from flask_login import current_user, login_required
from project.models.shop import Book, Author
from project.users.admin.forms import NewBookForm
from project import db

admin = Blueprint("admin", __name__)


@admin.route("/book/new/", methods=["POST", "GET"])
@login_required
def new_book():
    form = NewBookForm()

    if form.validate_on_submit():
        writer = Author.query.filter_by(name=form.author.data).first()
        
        if writer == None:
            new_author = Author(name=form.author.data)
            db.session.add(new_author)
            db.session.commit()
            writer = new_author
        
        book = Book(
            title = form.title.data,
            price = form.price.data,
            genre = form.genre.data,
            pages_num = form.pages_num.data,
            isbn = form.isbn.data,
            year_published = form.year_published.data,
            publisher = form.publisher.data,
            info = form.info.data,
            author_id = writer.id
        )
        
        db.session.add(book)
        db.session.commit()

        flash(Markup(f"Kniha <b>{form.title.data}</b> bola úspešne pridaná."), "success")
        return redirect(url_for("main.home"))

    return render_template("books/newBook.html", form=form, legend="Nová kniha")
