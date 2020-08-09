from flask import Blueprint, redirect, render_template, url_for, request, flash, Markup
from flask_login import current_user, login_user, logout_user, login_required
from project.users.account.forms import LoginForm, RegisterForm, EditAccountForm, ContactForm
from project.models.account import User, Info
from project import bcrypt, db
from project.models.account import Info

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

                return redirect(url_for("main.home"))
            else:
                flash(message=Markup("Zlé prihlasovacie meno alebo heslo. Ak ste zabudli svoje heslo, obnovte si ho <a href='#' class='alert-link'>tu</a>."), category="danger")

        return render_template("users/login.html", title="Prihlásenie", legend="Prihlásiť sa", form=form)



@account.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@account.route("/account/")
@login_required
def my_account():
    contact_info = Info.query.get(current_user.info_id)
    has_info = contact_info   
    return render_template("users/account.html", contact=contact_info, has_info=has_info)

@account.route("/account/edit/info/", methods=["GET", "POST"])
@login_required
def account_edit_info():
    
    
    


    return "BITCH"


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
        form.first_name.data = info.first_name
        form.last_name.data = info.last_name
        form.phone_number.data =info.phone_number
        form.city.data =info.city
        form.psc.data = info.psc
        form.house_number.data = info.house_number
        form.street.data = info.street

    return render_template("users/accountEdit.html", form=form, legend="Úprava kontaktných údajov")

@account.route("/account/edit/contact/new/", methods=["GET", "POST"])
@login_required
def account_edit_contact_new():
    form = ContactForm()
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