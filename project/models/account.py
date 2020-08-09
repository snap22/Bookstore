from project import login_manager, db
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# pouzivatel
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(130), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False) 
    #confirmed = db.Column(db.Boolean(), default=False, nullable=False)     #posle sa confirmation email a potom sa nastavi na true
    # link to the picture of the user
    picture = db.Column(db.String(50), nullable=False, default="Default.png")

    orders = db.relationship("Order", backref="ordered_items", lazy=True)

    info_id = db.Column(db.Integer, db.ForeignKey("info.id"), nullable=True)
    

    def __repr__(self):
        return f"User {self.username}, email={self.email}, picture={self.picture}"



#kontaktne udaje
class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False, default="Slovakia")
    city = db.Column(db.String(100), nullable=False)
    psc = db.Column(db.String(5), nullable=False)
    street = db.Column(db.String(80), nullable=False)
    house_number = db.Column(db.Integer, nullable=False)




