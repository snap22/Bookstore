from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_login import current_user

class PaymentForm(FlaskForm):
    first_name = StringField("Krstné meno", validators=[DataRequired(message="Toto pole je povinné")])
    last_name =  StringField("Priezvisko", validators=[DataRequired(message="Toto pole je povinné")])
    phone_number =  StringField("Telefónne číslo", validators=[DataRequired(message="Toto pole je povinné")])
    city =  StringField("Mesto", validators=[DataRequired(message="Toto pole je povinné")])
    street = StringField("Ulica", validators=[DataRequired(message="Toto pole je povinné")])
    house_number = IntegerField("Číslo domu", validators=[DataRequired(message="Toto pole je povinné")])
    psc = StringField("PSČ", validators=[DataRequired(message="Toto pole je povinné")])
    submit = SubmitField("Objednať")

    pay_type = RadioField("Spôsob platby", choices=[("4.99", "Dobierka - 4.99€"), ("0.00", "Bankovým prevodom - 0.00€")])
    delivery_type = RadioField("Spôsob doručenia", choices=[("3.99" ,"Kuriér - 3.99€"), ("2.49", "Slovenská pošta (na poštu) - 2.49€"), ("2.99", "Slovenská pošta (na adresu) - 2.99€")])

    def get_input_types(self):
        return [self.first_name, self.last_name, self.phone_number, self.city, self.street, self.house_number, self.psc]

    def validate_psc(self, psc):
        if (psc.data.strip().isdigit() and len(psc.data) == 5) == False:
            raise ValidationError(message="Zadajte správne PSČ bez medzier")

    def validate_phone_number(self, phone_number):
        if (phone_number.data.strip().isdigit() and len(phone_number.data) == 10)  == False:
            raise ValidationError(message="Zadajte správne telefónne číslo bez medzier")

