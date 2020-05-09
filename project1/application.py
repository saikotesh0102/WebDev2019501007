import os
import hashlib
import logging
import requests
from flask import Flask, session, render_template, request, redirect, url_for, jsonify,flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
from models import User, Book
from create import *
import datetime

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
            user = User(email, name, password, datetime.datetime.now())
            try: 
                db.session.add(user)
                db.session.commit()
                logging.debug("user successfully registered in db")
            except Exception as e:
                print(e)
                name = "Registration Unsuccessful. Please Register Again"
                return render_template("registration.html", name = name)
           
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
        return render_template("search.html")
    else:
        select = request.form.get('comp')
        result = request.form.get('search')
        # print(select,result,"----------------------------------")
        like_format = '%{}%'.format(select)
        if result == "":
            return render_template("search.html", msg="query is empty")
        else:
            if result == "on":
                data = db.session.query(Book).filter(Book.isbn.like(like_format)).order_by(Book.title).all()
            elif result == "title":
                data = db.session.query(Book).filter(Book.title.like(like_format)).order_by(Book.title).all()
            # elif result == "author":
            else:
                data = db.session.query(Book).filter(Book.author.like(like_format)).order_by(Book.title).all()
            #     # print(result)
            #     # print(type(result))
            #     result = str(result)
            #     # print(type(result))
            #     # select = int(select)
            #     # like_format = '%{}%'.format(select)
            #     data = db.session.query(Book).filter(Book.year.like(like_format)).order_by(Book.title).all()
                
            if len(data) == 0:
                return render_template("error.html")
            else:
                return render_template("search.html", data=data)


@app.route("/api/search",methods=['POST'])
def api_search():
    if request.is_json:
        tokens = request.get_json()
        searchType = tokens["type"].strip()
        if "type" in tokens and "search" in tokens and searchType in ['isbn','title','author']:
            searchQuery = tokens['search'].strip()
            results,message = search(searchType,searchQuery)
            if len(message)==0:
                lis = []
                for result in results:
                    b = {}
                    b["isbn"] = result.isbn
                    lis.append(b)
                resultJson = {}
                resultJson['Bookss'] = lis
                return jsonify(resultJson)
            return (jsonify({"Error":message}),400)
        return (jsonify({"Error":"Invaiid Request"}),400)
    else:
        return (jsonify({"Error":"Invaiid Request"}),400)


# @app.route("/home", methods = ["GET", "POST"])
# def home():
#     try:
#         text = "Welcome"+session.get("name")
#         if request.method == 'GET':
#             searchType = ['isbn', 'title', 'author','year']
#             try:
#                 return render_template("search.html", text=text,searchType = searchType)
#             except:
#                 flash("Please enter valid username and password")
#                 return render_template("registration.html")
#         else:
#             results,message = search(request.form["searchType"],request.form["search"])
#             return render_template('search.html',books = results,message = message)
#     except:
#         flash("User don't have an account")
#         return render_template("registration.html")


# @app.route("/api/book/", methods=["GET"])

# def api_get_book():
#     isbn = request.args.get('isbn') 
#     book = get_book(isbn)
#     response_book = bookreads_api(isbn)
#     if request.method == "GET":
#         if book.count() != 1:
#             logging.debug("invalid isbn number")
#             return (jsonify({"Error": "Invalid book ISBN"}), 422)
#         else:
#             book = book[0]
#             logging.debug("successfull in database query")
#             return jsonify(title=book.name, author=book.author, year=book.year, isbn=book.isbn, avg_ratings=response_book["average_rating"], img=response_book["img"])




# @app.route("/logout")
# def logout():
#     session.clear()
#     return render_template("registration.html", text="successfully logged out")

# @app.route("/book/<string:isbn>", methods = ["GET"])
# def get_book(isbn):
#     response = bookreads_api(isbn)
#     return db.session.query(Book).filter_by(isbn=isbn)
    

# def bookreads_api(isbn):
#     query = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "k6vmXaMXA30l0L8bAkZw", "isbns": isbn})
#     # response = query.json()
#     print("response:", query.text)
#     response = query
#     response = response['books'][0]
#     book_info = Book.query.get(isbn)
#     response = dict(response)
#     response['name'] = book_info[0][0]
#     response['author'] = book_info[0][1]
#     response['year'] = book_info[0][2]
#     response['img'] = "http://covers.openlibrary.org/b/isbn/" + str(isbn) + ".jpg"
    
#     # return response
#     return jsonify({"response":response})








            
 



    








    





