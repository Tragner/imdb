from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import hashlib
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/imdb'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32))
    active = db.Column(db.Boolean())
    token = db.Column(db.String(32))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = hashlib.md5(password.encode('utf-8')).hexdigest()
        self.active = False
        self.token = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()

    def __repr__(self):
        return '<User {0}>'.format(self.email)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    score = db.Column(db.Integer)
    year = db.Column(db.Integer)

    def __init__(self, name, score, year):
        self.name = name
        self.score = score
        self.year = year

    def __repr__(self):
        return '<Movie %r>' % self.name
