from project import lm, db


# odkomentovat to ked sa pridaju modely do databazy
""" 
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) """