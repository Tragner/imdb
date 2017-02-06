from flask import Flask, render_template, redirect, url_for
from forms import UserForm
from datetime import datetime
from models import User
from functools import wraps
import hashlib

app = Flask(__name__)
app.secret_key = 'secret'

@app.route("/")
def index():
    return redirect(url_for('signup'))

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = UserForm()
    return render_template('items/signin.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)