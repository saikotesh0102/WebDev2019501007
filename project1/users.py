from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

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