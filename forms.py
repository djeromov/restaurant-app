from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, RadioField
from wtforms.fields.core import IntegerField
from wtforms.validators import InputRequired, Length, NumberRange
from flask_wtf.file import FileField, FileAllowed



class LoginForm(FlaskForm):
    """Form for logging in."""

    username = StringField("Usuario",
        validators=[InputRequired()])
    password = PasswordField("Contraseña",
        validators=[InputRequired()])


class NewUserForm(FlaskForm):
    """Form for logging in."""

    username = StringField("Usuario",
        validators=[InputRequired(), Length(min=3, message='Minimo de 3 carácteres')])
    password = PasswordField("Contraseña",
        validators=[InputRequired(), Length(min=6, message='Minimo de 6 carácteres')])
    is_admin = RadioField("Administrador",
        choices=[(True, 'Si'), (False, 'No')],
        validators=[InputRequired()])


class ChangeMenuForm(FlaskForm):
    """Form for menu."""
    menu = TextAreaField("Menu",
        validators=[InputRequired(), Length(max=350, message='Maximo de 350 carácteres')])


class AddImageForm(FlaskForm):
    """Form for adding images."""

    photo_file = FileField("Añadir imagen",
        validators=[InputRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'bmp'], 'Formato de imagen esta invalido.')])


class WhatsappPhoneForm(FlaskForm):
    """Form for whatsapp #."""
    whatsapp_phone = IntegerField("Numero de WhatsApp",
        validators=[InputRequired(), NumberRange(min=1000000000, max=99999999999999, message='Entra un numero entre 10 y 14 numeros')])

