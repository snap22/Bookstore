from flask import Blueprint, redirect, render_template, url_for, request, flash, Markup
from flask_login import current_user, login_user, logout_user, login_required
from project.users.account.forms import LoginForm, RegisterForm, EditAccountForm, ContactForm, ChangePasswordForm, ChangePictureForm
from project.models.account import User, Info
from project import bcrypt, db
from project.models.shop import Order, Book
from project.users.account.utils import save_picture, remove_picture
from project.books.utils import clear_cart

account = Blueprint("account", __name__)

@account.route("/register/", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    else:
        form = RegisterForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash(message="Účet bol vytvorený úspešne", category="success")
            login_user(new_user, remember=True)
            return redirect(url_for("main.home"))

        return render_template("users/register.html", title="Registrácia", legend="Registrovať sa", form=form)

@account.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                flash(message="Prihlásenie prebehlo úspešne", category="success")
                login_user(user, remember=True)
                #check_admin(user)

                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
            else:
                flash(message=Markup("Zlé prihlasovacie meno alebo heslo. Ak ste zabudli svoje heslo, obnovte si ho <a href='#' class='alert-link'>tu</a>."), category="danger")

        return render_template("users/login.html", title="Prihlásenie", legend="Prihlásiť sa", form=form)



@account.route("/logout/")
@login_required
def logout():
    clear_cart()
    logout_user()
    return redirect(url_for("main.home"))


@account.route("/account/", methods=["GET", "POST"])
@login_required
def my_account():
    contact_info = Info.query.get(current_user.info_id)
    has_info = contact_info   

    form = ChangePictureForm()

    if request.method == "POST": 
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            remove_picture(current_user.picture)    #vymaze staru fotku

            current_user.picture = picture_file
            db.session.commit()
            flash("Fotka bola zmenená", "success")
            return redirect(url_for(request.endpoint))
        
    else:
        books = Book.query
        orders = enumerate(Order.query.filter_by(buyer_id=current_user.id).all())
    
    return render_template("users/account.html", contact=contact_info, has_info=has_info, form=form, orders=orders, books=books, round=round)

@account.route("/account/edit/info/", methods=["GET", "POST"])
@login_required
def account_edit_info():
    form = EditAccountForm()
    user = User.query.get(current_user.id)
    if request.method == "POST":
        if form.validate_on_submit():
            
            user.username = form.username.data
            user.email = form.email.data
            db.session.commit()
            flash("Údaje boli aktualizované", "success")
            return redirect(url_for("account.my_account"))
    else:
        form.username.data = user.username
        form.email.data = user.email

    return render_template("users/accountEdit.html", form=form, legend="Základné údaje")

@account.route("/account/edit/password/", methods=["GET", "POST"])
@login_required
def account_edit_password():
    form = ChangePasswordForm()
    user = User.query.get(current_user.id)
    if form.validate_on_submit():
        new_password = bcrypt.generate_password_hash(form.new_password.data) 
        user.password = new_password
        db.session.commit()
        flash("Heslo bolo zmenené", "success")
        return redirect(url_for("account.my_account"))

    return render_template("users/accountEdit.html", form=form, legend="Základné údaje")


# adresa

@account.route("/account/edit/contact/", methods=["GET", "POST"])
@login_required
def account_edit_contact():
    form = ContactForm()
    info_id = current_user.info_id
    info = Info.query.get(info_id)
    if info is None:
        return redirect(url_for("account.account_edit_contact_new"))

    if request.method == "POST":    #ak metoda je POST tak ulozi udaje z formulara
        if form.validate_on_submit():
            info.first_name = form.first_name.data
            info.last_name = form.last_name.data
            info.phone_number = form.phone_number.data
            info.city = form.city.data
            info.psc = form.psc.data
            info.house_number = form.house_number.data
            info.state = "Slovakia"
            info.street = form.street.data
            db.session.commit()

            flash("Kontaktné údaje boli uložené", "success")
            return redirect(url_for("account.my_account"))

    else:   #ak metoda je GET tak vyplni formular automaticky
        form.fill_in(info)

    return render_template("users/accountEdit.html", form=form, legend="Úprava kontaktných údajov")

@account.route("/account/edit/contact/new/", methods=["GET", "POST"])
@login_required
def account_edit_contact_new():
    form = ContactForm()
    if request.method == "POST":
        if form.validate_on_submit():
            new_info = Info.create_based_on_form_data(form)

            db.session.add(new_info)
            db.session.commit()
            current_user.info_id = new_info.id
            db.session.commit()

            flash("Kontaktné údaje boli uložené", "success")
            return redirect(url_for("account.my_account"))

    return render_template("users/accountEdit.html", form=form, legend="Kontaktné údaje")



""" 
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    psc = db.Column(db.String(5), nullable=False)
    street = db.Column(db.String(80), unique=True, nullable=False)
    house_number = db.Column(db.Integer, nullable=False)
 """