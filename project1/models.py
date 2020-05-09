from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'USERS'
	email = db.Column(db.String, primary_key = True)
	name = db.Column(db.String, nullable = False)
	password = db.Column(db.String, nullable = False)
	timestamp = db.Column(db.DateTime, nullable = False)
	
	def __init__(self, email, name, password,timestamp):
		self.email = email
		self.name = name
		self.password = password
		self.timestamp = timestamp
	
	# def __repr__(self):
	# 	return '<User %r>' % (self.email)

		
class Book(db.Model):
    __tablename__ = "BOOKSS"
    isbn = db.Column(db.String, primary_key = True)
    title = db.Column(db.String, nullable = False)
    author = db.Column(db.String, nullable = False)
    year = db.Column(db.Integer, nullable = False)

    def __init__(self, isbn, title, author, year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year

# db.create_all()
	# def __repr__(self):
	# 	return '<Book %r>' % (self.name)