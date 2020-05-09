
# import csv,os
# from flask import Flask, session
# from flask_session import Session
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from flask import render_template, request, session
# from flask_session import Session
# from flask_sqlalchemy import SQLAlchemy
# # from models import Book

# app1 = Flask(__name__)

# app1.config["SESSION_PERMANENT"] = False
# app1.config["SESSION_TYPE"] = "filesystem"
# Session(app1)



# app1.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# app1.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app1.app_context().push()
# db = SQLAlchemy()
# db.init_app(app1)


# # class Book(db.Model):
	
# #     __tablename__ = "BOOKS"
# #     isbn = db.Column(db.String, primary_key = True)
# #     title = db.Column(db.String, nullable = False)
# #     author = db.Column(db.String, nullable = False)
# #     year = db.Column(db.Integer, nullable = False)

# #     def __init__(self, isbn, title, author, year):
# #         self.isbn = isbn
# #         self.title = title
# #         self.author = author
# #         self.year = year

# db.create_all()
# # def __repr__(self):
# #      return '<Book %r>' % (self.name)
# def main():
#     print("dfghjk----------")
#     b = open("books.csv")
#     print("gthrhyhyt-------------------")
#     books = csv.reader(b)
#     i = 0
#     for ISBN, title, author, year in books:
#         if i != 0:
#             book = Book(isbn=ISBN, title=title, author=author, year=year)
#             print(book.title)
#             db.session.add(book)
#         i = i + 1
#     db.session.commit()

# if __name__ == "__main__":
#     main()

"""
importing data from books.csv to postgresql
"""
import os, csv
from flask import Flask, render_template, request
from models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
"""
main method to create table and insert data.
"""
def main():
	#to create the table.
    db.create_all()
    #reading the file and insertion data into database.
    with open("books.csv", 'r') as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            newBook = Book(row[0], row[1], row[2], int(row[3]))
            db.session.add(newBook)
    db.session.commit()

if __name__ == "__main__":
  with app.app_context():
      main()










