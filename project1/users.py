from datetime import datetime
from sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = ("USERS")
    email = db.Column(db.String, primary_key = True)
    firstname = db.Column(db.String, nullable = False)
    lastname = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    timestamp = db.Column(db.DateTime, nullable = False)

    def __init__(self, email, firstname, lastname, password, gender):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.timestamp = datetime.now()