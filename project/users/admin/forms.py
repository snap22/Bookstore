from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, TextAreaField, IntegerField, SelectField
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
    language = StringField("Jazyk", validators=[DataRequired(), Length(2, 100)])
    info = TextAreaField("Obsah knihy", validators=[DataRequired()])
    
    submit = SubmitField("Pridať knihu")

        
class FindBookForm(FlaskForm):
    name = StringField("Názov knihy")
    submit = SubmitField("Hľadať")

class GenBookForm(FlaskForm):
    select = SelectField("", choices=[(0, "Žiadne výsledky zatiaľ")], coerce=int, default=0)
    submit = SubmitField("Pokračovať")