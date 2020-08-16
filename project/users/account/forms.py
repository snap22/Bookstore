from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_login import current_user
from project.models.account import User
from project import bcrypt

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

class ContactForm(FlaskForm):
    first_name = StringField("Krstné meno", validators=[DataRequired(message="Toto pole je povinné")])
    last_name =  StringField("Priezvisko", validators=[DataRequired(message="Toto pole je povinné")])
    phone_number =  StringField("Telefónne číslo", validators=[DataRequired(message="Toto pole je povinné")])
    city =  StringField("Mesto", validators=[DataRequired(message="Toto pole je povinné")])
    street = StringField("Ulica", validators=[DataRequired(message="Toto pole je povinné")])
    house_number = IntegerField("Číslo domu", validators=[DataRequired(message="Toto pole je povinné")])
    psc = StringField("PSČ", validators=[DataRequired(message="Toto pole je povinné")])
    submit = SubmitField("Uložiť")

    def validate_psc(self, psc):
        if (psc.data.strip().isdigit() and len(psc.data) == 5) == False:
            raise ValidationError(message="Zadajte správne PSČ bez medzier")

    def validate_phone_number(self, phone_number):
        if (phone_number.data.strip().isdigit() and len(phone_number.data) == 10)  == False:
            raise ValidationError(message="Zadajte správne telefónne číslo bez medzier")

    def fill_in(self, info):
        try:
            self.first_name.data = info.first_name
            self.last_name.data = info.last_name
            self.phone_number.data = info.get_phone_number()
            self.city.data = info.city
            self.street.data = info.street
            self.house_number.data = info.house_number
            self.psc.data = info.get_psc()
        except AttributeError:  #ak je nespravny model pouzity vo formulari
            return


class EditAccountForm(FlaskForm):
    username = StringField("Používateľské meno", validators=[DataRequired(message="Toto pole je povinné")])
    email = StringField("Email", validators=[DataRequired(message="Toto pole je povinné"), Email(message="Použite platný email")])
    submit = SubmitField("Uložiť")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Toto používateľské meno je už obsadené.")
        

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Tento email je už obsadený.")
        
class ChangePictureForm(FlaskForm):
    picture = FileField("Profilová fotka", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Uložiť")

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Pôvodné heslo", validators=[DataRequired(message="Toto pole je povinné")])
    new_password = PasswordField("Nové heslo", validators=[DataRequired(message="Toto pole je povinné")])
    confirm_new_password = PasswordField("Potvrdenie nového hesla", validators=[DataRequired(message="Toto pole je povinné"), EqualTo("new_password", message="Heslá musia byť rovnaké")])
    submit = SubmitField("Uložiť")

    #Vráti bool či sa aktualne heslo pouzivatela rovna heslu ktore zadal do fieldu
    def __check_password(self, password_field):
        return bcrypt.check_password_hash(current_user.password, password_field.data)
    
    
    def validate_new_password(self, new_password):
        if self.__check_password(new_password):
            raise ValidationError("Zvoľte si iné heslo.")

    def validate_current_password(self, current_password):
        if not self.__check_password(current_password):
            raise ValidationError("Toto heslo nie je platné")

    