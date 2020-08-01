from project.models.account import User
from project.models.admin import Admin
from flask import session, abort

# pozrie sa ci je id uzivatela v databaze adminov, ak hej prida ho do session
def check_admin(user):
    found_admin = Admin.query.filter_by(user_id=user.id).first()
    if found_admin:
        session["admin"] = found_admin

# pozrie sa ci je admin
def is_admin():
    return "admin" in session

# odhlasi admina ak je
def logout_admin():
    if is_admin():
        session.pop("admin", None)


