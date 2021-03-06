from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length, Email, DataRequired, NumberRange
from datetime import datetime

class UserForm(Form):
    username = StringField('Username', validators=[InputRequired('Campo Nombre Obligatorio'),
                                             Length(1, 100, 'Texto inferior a 100 caracteres')])
    email = StringField('Email', validators=[InputRequired('Campo Email Obligatorio'),
                                             Length(1, 100, 'Texto inferior a 100 caracteres'),
                                             Email('Correo incorrecto')])
    password = PasswordField('Contraseña', validators=[InputRequired('Por favor, escribe una contraseña')])
    password2 = PasswordField('Repetir Contraseña', validators=[InputRequired('Por favor, escribe de nuevo la contraseña')])
    submit = SubmitField('Submit')

class UserForm(Form):
    username = StringField('Username', validators=[InputRequired('Campo Nombre Obligatorio'),
                                             Length(1, 100, 'Texto inferior a 100 caracteres')])
    email = StringField('Email', validators=[InputRequired('Campo Email Obligatorio'),
                                             Length(1, 100, 'Texto inferior a 100 caracteres'),
                                             Email('Correo incorrecto')])
    password = PasswordField('Contraseña', validators=[InputRequired('Por favor, escribe una contraseña')])
    password2 = PasswordField('Repetir Contraseña', validators=[InputRequired('Por favor, escribe de nuevo la contraseña')])
    submit = SubmitField('Submit')

class MovieForm(Form):
    name = StringField('Name', validators=[InputRequired('Campo Nombre Obligatorio'),
                                             Length(1, 100, 'Texto inferior a 100 caracteres')])
    year = IntegerField('Year', validators=[DataRequired('Campo año obligatorio'),
                                              NumberRange(1850, datetime.now().year, 'Año a partir de 1850')])
    score = IntegerField('Score', validators=[DataRequired('Campo puntuacion obligatorio'),
                                              NumberRange(0, 10, 'Puntuacion entre 0 y 10')])
    submit = SubmitField('Add')

class SearchForm(Form):
    name = StringField('Name', validators=[Length(1, 100, 'Texto inferior a 100 caracteres')])
    year = IntegerField('Year', validators=[NumberRange(1850, datetime.now().year, 'Año a partir de 1850')])
    submit = SubmitField('Search')
