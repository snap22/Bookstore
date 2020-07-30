from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_login import current_user
from project.models.shop import Book, Author
from project import db

class NewBookForm(FlaskForm):
    title = StringField("Názov knihy", validators=[DataRequired(), Length(2, 200)])
    author = StringField("Autor", validators=[DataRequired()])
    price = FloatField("Cena", validators=[DataRequired()])
    genre = StringField("Žáner", validators=[DataRequired(), Length(2, 200)])
    isbn = StringField("ISBN", validators=[DataRequired(), Length(2, 30)])
    pages_num = IntegerField("Počet strán",validators=[DataRequired()])
    year_published = IntegerField("Rok vydania",validators=[DataRequired()])
    publisher = StringField("Vydavateľ", validators=[DataRequired(), Length(2, 100)])
    info = TextAreaField("Obsah knihy", validators=[DataRequired()])
    submit = SubmitField("Pridať knihu")

    def validate_title(self, title):
        book = Book.query.filter_by(title=title.data).first()
        if book:
            raise ValidationError("Kniha s týmto názvom už je v databáze")

    
        



"""
title = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    genre = db.Column(db.String(200), nullable=False)
    pages_num = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(30), nullable=False)
    year_published = db.Column(db.Integer)
    publisher = db.Column(db.String(100), nullable=False)   
    picture = db.Column(db.String(20), nullable=False, default="Default.png")   #obrazok pre knihu
    language = db.Column(db.String(40), nullable=False, default="Slovenský")
"""