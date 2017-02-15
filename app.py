from flask import Flask, render_template, redirect, url_for, request, flash, session
from forms import UserForm, MovieForm, SearchForm
from models import User, Movie, db
from flask_mail import Mail, Message
from functools import wraps
import hashlib
import math

app = Flask(__name__)
app.secret_key = 'secret'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USERNAME'] = 'sarahtragner@gmail.com'
app.config['MAIL_PASSWORD'] = 'eelldasah99'
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
LIMITE_PELICULAS = 5

@app.route("/")
def login():
    form = UserForm()
    if request.args.get('email') and request.args.get('password'):
        email = request.args.get('email')
        password = hashlib.md5(request.args.get('password').encode('utf-8')).hexdigest()
        my_user = User.query.filter_by(email=email, password=password).first()
        if my_user:
            # Existe
            session['user'] = my_user.email
            return redirect(url_for('dashboard'))
        else:
            # Mostramos error
            flash('Su email o contraseña no es correcto', 'danger')
    return render_template('items/login.html', form=form)

@app.route('/close')
def close_session():
    session.clear()
    return redirect(url_for('dashboard'))

@app.route("/peliculas/", methods=['GET', 'POST'], defaults={'pag': 1})
@app.route("/peliculas/<int:pag>", methods=['GET', 'POST'])
def dashboard(pag=1):
    form = MovieForm()
    form_search = SearchForm();
    if request.method == 'POST':
        if form.validate_on_submit():
            movie = Movie(request.form['name'], request.form['score'], request.form['year'])
            db.session.add(movie)
            flash('Añadido correctamente', 'success')
            try:
                db.session.commit()
            except:
                db.session.rollback()
            return redirect(url_for('dashboard'))
        else:
            todos_errores = form.errors.items()
            for campo, errores in todos_errores:
                for error in errores:
                    flash(error, 'danger')
    num_movies = Movie.query.count()
    num_paginas = math.ceil(num_movies / LIMITE_PELICULAS)
    movies = Movie.query.limit(LIMITE_PELICULAS * pag).offset(LIMITE_PELICULAS * (pag - 1)).all()
    return render_template('items/dashboard.html', form=form, movies=movies, num_paginas=num_paginas, form_search=form_search)

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    form = UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = request.form['email']
            password = hashlib.md5(request.form['password'].encode('utf-8')).hexdigest()
            my_user = User.query.filter_by(email=email).first()
            if not my_user:
                if request.form['password'] == request.form['password2']:
                    my_user = User(request.form['username'], request.form['email'],
                                   request.form['password'])
                    db.session.add(my_user)
                    try:
                        db.session.commit()
                        # Envio de email
                        msg = Message("Hello",
                                      sender="no-reply@idecrea.com",
                                      recipients=[my_user.email])
                        link_token = f'http://localhost:5000/confirmar/{my_user.token}'
                        msg.html = render_template('mailing/confirmar.html',
                                                   link_token=link_token)
                        mail.send(msg)
                        # Informamos al usuario
                        flash('Confirmar email en su bandeja de entrada', 'success')
                    except:
                        db.session.rollback()
                        flash('Disculpe, ha ocurrido un error', 'danger')
                    return redirect(url_for('login'))
                else:
                    flash('Las contraseñas no coinciden', 'danger')
            else:
                flash('El email ya está registrado', 'danger')
        else:
            todos_errores = form.errors.items()
            for campo, errores in todos_errores:
                for error in errores:
                    flash(error, 'danger')
    return render_template('items/signin.html', form=form)
@app.route("/search/<ordenar>")
def search(ordenar):
    form = MovieForm()
    form_search = SearchForm();
    if ordenar == 'year':
        movies = Movie.query.order_by(Movie.year)
    return render_template('items/dashboard.html', movies=movies, form=form, form_search=form_search, num_paginas=0)



@app.route("/confirmar/<token>", methods=['GET', 'POST'])
def confirmar(token):
    my_user = User.query.filter_by(token=token).first()
    if my_user:
        my_user.active = True
        db.session.add(my_user)
        try:
            flash('Su cuenta ha sido activada', 'success')
            db.session.commit()
        except:
            db.session.rollback()
    else:
        flash('Enlace caducado', 'danger')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
