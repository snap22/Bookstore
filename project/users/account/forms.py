from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_login import current_user
from project.models import User

class RegisterForm(FlaskForm):
    username = StringField("Používateľské meno", validators=[DataRequired(message="Toto pole je povinné"), Length(3, 30, message="Vyberte si uživateľské meno ktoré má aspoň 3 a najviac 30 znakov")])
    email = StringField("Email", validators=[DataRequired(message="Toto pole je povinné"), Email(message="Použite platný email")])
    password = PasswordField("Heslo", validators=[DataRequired(message="Toto pole je povinné")])
    confirm_password = PasswordField("Potvrdenie hesla", validators=[DataRequired(message="Toto pole je povinné"), EqualTo("password", message="Heslá musia byť rovnaké")])
    submit = SubmitField("Registrovať sa")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Toto používateľské meno je už obsadené. Zvoľte si iné")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Tento email je už obsadený. Zvoľte si iný")

class LoginForm(FlaskForm):
    username = StringField("Používateľské meno", validators=[DataRequired(message="Toto pole je povinné")])
    password = PasswordField("Heslo", validators=[DataRequired(message="Toto pole je povinné")])
    submit = SubmitField("Prihlásiť sa")

#update account info + adresa
#reset hesla