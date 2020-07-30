from project import login_manager, db
from flask_login import UserMixin
from datetime import datetime



#   ----- UZIVATEL -----


""" @login_manager.user_loader
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

    address_id = db.Column(db.Integer, db.ForeignKey("address.id"), nullable=True)  #adresa nie je povinna pri registracii uzivatela

    def __repr__(self):
        return f"User {self.username}, email={self.email}, picture={self.picture}"

# adresa
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(30), unique=True, nullable=False)
    city = db.Column(db.String(80), unique=True, nullable=False)
    psc = db.Column(db.String(5), nullable=False)
    street = db.Column(db.String(80), unique=True, nullable=False)
    house_number = db.Column(db.Integer, nullable=False)

    inhabitants = db.relationship("User", backref="users", lazy=True)
 """
#   ----- UZIVATELSKE VECI -----

""" class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
 """

#   ------ OBCHOD ------


""" # tabulka pre many-to-many relationship
transactions = db.Table("transactions", 
    db.Column("order_id", db.Integer, db.ForeignKey("order.id")),
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"))
)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    books = db.relationship("Book", backref="writer", lazy=True)

    def __repr__(self):
        return f"Author {self.name}"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    genre = db.Column(db.String(200), nullable=False)
    pages_num = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(30), nullable=False)
    year_published = db.Column(db.Integer)
    publisher = db.Column(db.String(100), nullable=False)   
    picture = db.Column(db.String(20), nullable=False, default="Default.png")   #obrazok pre knihu
    language = db.Column(db.String(40), nullable=False, default="Slovenský")
    info = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)

    def __repr__(self):
        return f"Book {self.title}, genre={self.genre}, price={self.price}"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    buyer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    books = db.relationship("Book", secondary=transactions , backref=db.backref("orders", lazy="dynamic"))

    def __repr__(self):
        return f"Order num:{self.number}"

 """



