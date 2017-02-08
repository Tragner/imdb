from flask import Flask, render_template, redirect, url_for, request, flash
from forms import UserForm
from models import User, db
from flask_mail import Mail, Message
from functools import wraps
import hashlib
app = Flask(__name__)
app.secret_key = 'secret'
mail = Mail(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['USER_MAIL'] = 'sarahtragner@gmail.com'
app.config['USER_PASSWORD'] = '99'



@app.route("/")
def login():
    msg = Message("Hello",
                  sender="no-reply@idecrea.com",
                  recipients=["sarahtragner@gmail.com"])
    mail.send(msg)
    return render_template('items/login.html')


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    form = UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = request.form['email']
            my_user = User.query.filter_by(email=email).first()
            if not my_user:
                if request.form['password'] == request.form['password2']:
                    my_user = User(request.form['username'], request.form['email'],
                                   request.form['password'])
                    db.session.add(my_user)
                    try:
                        db.session.commit()
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


if __name__ == "__main__":
    app.run(debug=True)
