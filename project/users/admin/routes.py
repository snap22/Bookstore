from flask import Blueprint, url_for, render_template, redirect, flash, session, abort, Markup, request
from flask_login import current_user, login_required
from project.models.shop import Book, Author
from project.users.admin.forms import NewBookForm, FindBookForm, GenBookForm
from project import db

admin = Blueprint("admin", __name__)

@admin.route("/book/gen/", methods=["POST", "GET"])
@login_required
def gen_book():
    findForm = FindBookForm()
    genForm = GenBookForm() 
    
    if "found_choices" in session:
        x = Book.query.all()
        genForm.select.choices = [(book.id, book.title) for book in x]
    
    if request.method == "POST":
        if findForm.validate_on_submit() and findForm.name.data:
            flash("Continuing bitch", "info")
            
            session["found_choices"] = "wii"
            
            return redirect(url_for("admin.gen_book"))
        
        if genForm.validate_on_submit() and genForm.select.data:
            flash(f"Selected {genForm.select.data}", "warning")

            session.pop("found_choices", None)
            return redirect(url_for("admin.gen_book"))

    return render_template("admin/bookGen.html", find_form = findForm, gen_form = genForm)





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
