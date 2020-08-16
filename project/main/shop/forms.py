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
        data = self.__remove_empty_spaces(psc)
        if not (data.isdigit() and len(data) == 5):     #ak je psc viac ako 5 cilic alebo v psc su pismena
            raise ValidationError(message="Zadajte správne PSČ")

    def validate_phone_number(self, phone_number):
        data = self.__remove_empty_spaces(phone_number)
        if not (data.isdigit() and len(data) == 10):    #ak su v telefonnom cisle pismena alebo ma viac ako 10 cislic
            raise ValidationError(message="Zadajte správne telefónne v tvare 0xxx xxx xxx")

    def __remove_empty_spaces(self, field):
        new_data = field.data.replace(" ", "")
        return new_data
    
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
        