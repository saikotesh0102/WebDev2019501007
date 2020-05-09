import os
import hashlib
import logging
import requests
from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
from models import User, Book
from create import *

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
logging.basicConfig(filename = 'logger.log', level = logging.DEBUG)

# Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
logging.debug("database sessions created")

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "GET":
        if session.get('data') is not None:
            return render_template("dashboard.html", name = session.get("data"))
        return redirect(url_for("login"))

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('data') is not None:
            return render_template("dashboard.html", name = session.get("data"))
        return render_template("main.html")

#registration page
@app.route("/register", methods = ['GET', 'POST'])
def register():
    """register a user in to database"""
    if request.method == 'GET':
        return render_template("registration.html")
    elif request.method == 'POST':
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        name = fname + " " + lname
        email = request.form.get('email')
        pwd = request.form.get('password')
        password = hashlib.md5(pwd.encode()).hexdigest()
        repwd = request.form.get('repassword')
        repassword = hashlib.md5(repwd.encode()).hexdigest()
        if password == repassword:
            user = User(email, name, password)
            try:
                db.session.add(user)
                logging.debug("user successfully registered in db")
            except:
                name = "Registration Unsuccessful. Please Register Again"
                return render_template("registration.html", name = name)
            db.session.commit()
            return redirect(url_for("login"))
        else:
            name = "Entered Passwords Do Not Match. Please Register Again"
            return render_template("registration.html", name = name)

@app.route("/admin")
def admin():
    users = User.query.order_by("timestamp").all()
    return render_template("admin.html", users = users)

@app.route("/auth", methods = ["POST"])
def verify():
    email = request.form.get('email')
    pwd = request.form.get('password')
    password = hashlib.md5(pwd.encode()).hexdigest()
    user = User.query.get(email)
    if user is not None:
        if email == user.email and password == user.password:
            fullname = user.name
            session["data"] = email
            logging.debug("User Loggedin Successfully")
            name = "Thank You for Logging In"
            return render_template("dashboard.html", name = name + " " + fullname)
    return redirect(url_for("register"))

@app.route("/logout")
def logout():
    session.clear()
    logging.debug("User Logged out Successfully")
    return redirect(url_for("login"))
    

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == "GET":
        postsearch = False
        if 'name' not in session:
            return render_template("search.html")
    else:
        postsearch = True
        select = request.form.get('comp')
        result = request.form.get('search')
        like_format = '%{}%'.format(result)
        if result == "":
            return render_template("search.html", msg="query is not empty")
        else:
            if select == "ISBN":
                data = db.session.query(Book).filter(Book.isbn.like(like_format)).order_by(Book.title).all()
            elif select == "Title":
                data = db.session.query(Book).filter(Book.title.like(like_format)).order_by(Book.title).all()
            elif select == "Author":
                data = db.session.query(Book).filter(Book.author.like(like_format)).order_by(Book.title).all()
            else:
                data = db.session.query(Book).filter(Book.year.like(like_format)).order_by(Book.title).all()
                
            if len(data) == 0:
                return render_template("search.html", message="Provide available data")
            
            else:
                return render_template("search.html", data=data)



# @app.route("/book/<string:isbn>", methods = ["GET"])
# def get_book(isbn):
#     response = bookreads_api(isbn)
#     return render_template("bookpage.html", 
#                 name=response["name"], 
#                 author=response["author"], 
#                 ISBN = response["isbn"], 
#                 year=response["year"], 
#                 rating=float(response["average_rating"]), 
#                 count=float(response["reviews_count"]))
                
# def bookreads_api(isbn):
#     logging.debug(session.get('data'))
#     # result = db.execute("SELECT title, author, year FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
#     res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "", "isbns": isbn})
#     print(res.text)
#     response = res.json()
#     book_details = res.json()
#     print(book_details)
#     key = ['title', 'author', 'year', 'isbn',
#             'review_count', 'average_score', 'rating_count']
#     values = [result[0][0], result[0][1], result[0][2], isbn, book_details['books']
#             [0]['reviews_count'], book_details['books'][0]['average_rating'], book_details['books'][0]['review_count']]
#     response = dict(zip(key, values))
#     logging.error(response)
#     return response
    



            
 



    








    




