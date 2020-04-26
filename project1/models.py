import os, datetime
from datetime import datetime
from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, PrimaryKeyConstraint

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy()
db.init_app(app)

class User(db.Model):
	__tablename__ = 'USERS'
	email = db.Column(db.String, primary_key = True)
	name = db.Column(db.String, nullable = False)
	password = db.Column(db.String, nullable = False)
	timestamp = db.Column(db.DateTime, nullable = False)
	
	def __init__(self, email, name, password):
		self.email = email
		self.name = name
		self.password = password
		self.timestamp = datetime.now()
	
	def __repr__(self):
		return '<User %r>' % (self.email)

class Book(db.Model):
    __tablename__ = "BOOKS"
    isbn = db.Column(db.String, primary_key = True)
    title = db.Column(db.String, nullable = False)
    author = db.Column(db.String, nullable = False)
    publicationyear = db.Column(db.Integer, nullable = False)

    def __init__(self, isbn, title, author, publicationyear):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publicationyear = publicationyear

class Review(db.Model):
	__tablename__ = 'REVIEWS'
	email = db.Column(db.String, ForeignKey("USERS.email"))
	isbn = db.Column(db.String, ForeignKey("BOOKS.isbn"))
	rating = db.Column(db.Integer, nullable = True, default = 0)
	review = db.Column(db.String, nullable = True)
	timestamp = db.Column(db.DateTime, nullable = False)

	def __init__(self, email, isbn, rating, review):
		self.email = email
		self.isbn = isbn
		self.rating = rating
		self.review = review
		self.timestamp = datetime.now()
	
	__table_args__ = (PrimaryKeyConstraint("isbn", "email"),)
	
with app.app_context():
	db.create_all()
	db.session.commit()