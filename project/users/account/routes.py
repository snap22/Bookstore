from flask import Blueprint, redirect, render_template, url_for, request, flash, Markup
from flask_login import current_user, login_user, logout_user, login_required
from project.users.account.forms import LoginForm, RegisterForm
from project.models import User
from project import bcrypt, db

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
                return redirect(url_for("main.home"))
            else:
                flash(message=Markup("Zlé prihlasovacie meno alebo heslo. Ak ste zabudli svoje heslo, obnovte si ho <a href='#' class='alert-link'>tu</a>."), category="danger")

        return render_template("users/login.html", title="Prihlásenie", legend="Prihlásiť sa", form=form)


@login_required
@account.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("main.home"))