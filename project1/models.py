from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from bookimport import *

db = SQLAlchemy()

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

class Review(db.Model):
	__tablename__ = 'REVIEWS'
	email = db.Column(db.String, db.ForeignKey("USERS.email"),primary_key = True)
	isbn = db.Column(db.String, db.ForeignKey("BOOKS.isbn"), primary_key = True)
	rating = db.Column(db.Integer, nullable = True, default=0)
	review = db.Column(db.String, nullable = True)
	timestamp = db.Column(db.DateTime, nullable = False)

	def __init__(self, email, isbn, rating, review):
		self.email = email
		self.isbn = isbn
		self.rating = rating
		self.review = review
		self.timestamp = datetime.now()