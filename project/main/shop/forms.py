from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_login import current_user

class PaymentForm(FlaskForm):
    #kontaktne udaje
    pass