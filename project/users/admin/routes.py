from flask import Blueprint, url_for, render_template, redirect, flash, session, abort, Markup, request
from flask_login import current_user, login_required
from project.models.shop import Book, Author
from project.users.admin.forms import NewBookForm, FindBookForm, GenBookForm
from project import db
from project.utils.webscrape import SearchScrape, BookInfoGenerator
from project.models.search import FoundBookInfo, Result

admin = Blueprint("admin", __name__)

@admin.route("/book/gen/", methods=["POST", "GET"])
@login_required
def gen_book():
    findForm = FindBookForm()
    genForm = GenBookForm() 

    #genForm.select.choices = [(book.id, book.title) for book in Book.query.all() -> store in var]
    if "found_id" in session:
        
        found_books = FoundBookInfo.query.filter_by(result_id=session["found_id"]).all()
        genForm.select.choices = [(book.id, book.description) for book in found_books]  #!!! aby to fungovalo, lebo ak select=0 tak sa nic nedeje
    if request.method == "POST":
        #Klikne na hladat
        if findForm.validate_on_submit() and findForm.name.data:   
            keywords = findForm.name.data
            flash(Markup(f"Našlo výsledky pre <b> { keywords }</b>"), "info")

            result = Result.query.filter_by(searched_words=keywords).first()  #skusi pohladat v databaze ci uz boli vyhladavanie tieto slova
            if result:
                session["found_id"] = result.id
            elif result is None:  #ak neboli
                flash("Pridané do databázy", "primary")
                new_result = Result(searched_words=keywords)
                db.session.add(new_result)
                db.session.commit()

                searcher = SearchScrape()
                searcher.search(keywords)   #vyhlada info
                found_books_choices = searcher.get_items()
                found_books = enumerate(found_books_choices)
                for index, found_book in found_books:  #pre kazde info co naslo tak to hodi do databazy
                    new_info = FoundBookInfo(description=found_book.info, link=found_book.link, result_id=new_result.id, choice_num=index)
                    db.session.add(new_info)
                
                db.session.commit()

                session["found_id"] = new_result.id

            
            return redirect(url_for("admin.gen_book"))
        
        if genForm.validate_on_submit() and genForm.select.data:    #ak sa klikne na tlacitko pokracovat
            flash(f"Selected {genForm.select.data}", "warning")
            if genForm.select.data is None:
                return redirect(url_for("admin.gen_book"))

            session.pop("found_id", None)
            
            return redirect(url_for("admin.new_book", gen_book_id=genForm.select.data))   #!!! hore sa pricitalo 1, tu sa musi odcitat

    return render_template("admin/bookGen.html", find_form = findForm, gen_form = genForm)



@admin.route("/book/new/")
@login_required
def new_book_basic():
    return redirect(url_for("admin.new_book", gen_book_id=0))

@admin.route("/book/new/generateID=<int:gen_book_id>", methods=["POST", "GET"])
@login_required
def new_book(gen_book_id):
    form = NewBookForm()

    if gen_book_id > 0:    #to bude vtedy ak chcem vygenerovat knihu, inak bude vsade -1
        
        generated_book = FoundBookInfo.query.get(gen_book_id)
        if generated_book is None:  #ak sa nenasla kniha s takymto id
            flash("Link s takýmto id sa nenašiel", "danger")
            return redirect(url_for("admin.gen_book"))

        txt = generated_book.description
        if "---" in txt:
            book_name, author_name = generated_book.description.split("---")
        else:
            book_name = generated_book.description.split("  -  ")[0]
        book_in_db = Book.query.filter_by(title=book_name.strip()).first()

        if book_in_db:
            flash("Táto kniha už je v databáze", "primary")
            return redirect(url_for("admin.edit_book", book_id=book_in_db.id))
        else:
            generator = BookInfoGenerator()
            generator.generate_data(generated_book.link)
            generator.fill_in_form(form)

    if form.validate_on_submit(): 
        writer = Author.query.filter_by(name=form.author.data).first()
        #ak autor nie je v databaze tak ho tam prida
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
            author_id = writer.id,
            language = form.language.data
        )
        
        db.session.add(book)
        db.session.commit()

        flash(Markup(f"Kniha <b>{form.title.data}</b> bola úspešne pridaná."), "success")
        return redirect(url_for("main.home"))

    return render_template("books/newBook.html", form=form, legend="Nová kniha")


@admin.route("/book/<int:book_id>/edit", methods=["GET", "POST"])
@login_required
def edit_book(book_id):
    found_book = Book.query.get(book_id)
    if found_book is None:
        flash("Takáto kniha nie je v databáze", "danger")
        return redirect(url_for("admin.gen_book"))
    
    form = NewBookForm()
    #form.submit.text = "Upraviť"
    # ak sa submitne button tak sa aktualizuju vsetky informacie o knihe na zaklade vyplneneho formulara
    if form.validate_on_submit():
        writer = Author.query.filter_by(name=form.author.data).first()
        #ak autor nie je v databaze tak ho tam prida
        if writer == None:
            new_author = Author(name=form.author.data)
            db.session.add(new_author)
            writer = new_author
            db.session.commit()

        found_book.title = form.title.data
        found_book.price = form.price.data
        found_book.genre = form.genre.data
        found_book.pages_num = form.pages_num.data
        found_book.isbn = form.isbn.data
        found_book.year_published = form.year_published.data
        found_book.info = form.info.data
        found_book.author_id = writer.id
        found_book.language = form.language.data
        found_book.publisher = form.publisher.data
        
        db.session.commit()
        flash(Markup(f"Kniha <b>{form.title.data}</b> bola upravená."), "success")
        return redirect(url_for("books.book", book_id=found_book.id))

    # ak sa len nacita stranka (t.j GET metoda) tak sa formular vyplni podla udajov o knihe
    elif request.method == "GET":
        #vyplni formular
        form.title.data = found_book.title
        form.price.data = found_book.price
        form.genre.data = found_book.genre
        form.pages_num.data = found_book.pages_num
        form.isbn.data = found_book.isbn
        form.year_published.data = found_book.year_published
        form.info.data = found_book.info
        form.author.data = Author.query.get(found_book.author_id).name
        form.language.data = found_book.language
        form.publisher.data = found_book.publisher

    return render_template("books/newBook.html", form=form, legend="Úprava informácií o knihe")

@admin.route("/book/<int:book_id>/delete", methods=["GET", "POST"])
@login_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        flash(Markup(f"Kniha <b>{book.title}</b> bola vymazaná."), "info")
    else:
        flash("Takúto knihu nemáme", "danger")
    return redirect(url_for("main.home"))