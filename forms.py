from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email

class UserForm(Form):
    email = StringField('Email', validators=[InputRequired('Campo Email Obligatorio'),
                                             Length(1, 100, 'Texto inferior a 100 caracteres'),
                                             Email('Correo incorrecto')])
    password1 = PasswordField('Contraseña', validators=[InputRequired('Por favor, escribe una contraseña')])
    password2 = PasswordField('Repetir Contraseña', validators=[InputRequired('Por favor, escribe de nuevo la contraseña')])
    submit = SubmitField('Submit')