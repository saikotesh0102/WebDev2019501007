import csv,os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from models import Book

db = SQLAlchemy()

def main():
    b = open("books.csv")
    books = csv.reader(b)
    i = 0
    for ISBN, title, author, publicationyear in books:
        if i != 0:
            book = Book(isbn=ISBN, title=title, author=author, publicationyear=publicationyear)
            print(book.title)
            db.session.add(book)
        i = i + 1
    db.session.commit()

if __name__ == "__main__":
    main()