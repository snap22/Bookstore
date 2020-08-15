from project import db
from datetime import datetime
from secrets import token_urlsafe
# tabulka pre many-to-many relationship
transactions = db.Table("transactions", 
    db.Column("order_id", db.Integer, db.ForeignKey("order.id")),
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"))
)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    books = db.relationship("Book", backref="writer", lazy="dynamic")

    def __repr__(self):
        return f"Author {self.name}"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    genre = db.Column(db.String(200), nullable=False, default="Neuvedený")
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
    name = db.Column(db.String(16), nullable=False, default=token_urlsafe(16))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    buyer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)  #ak je anonymny tak id bude 0
    info_id = db.Column(db.Integer, db.ForeignKey("info.id"), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)

    books = db.relationship("Book", secondary=transactions , backref=db.backref("orders", lazy="dynamic"))

    def __repr__(self):
        return f"Order num:{self.number}"


