import os, hashlib, logging, requests
from flask import Flask, session, render_template, request, redirect, url_for, json, jsonify
from flask_session import Session
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
from models import *

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
logging.basicConfig(filename = 'logger.log', level = logging.DEBUG)
logging.debug("database sessions created")

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "GET":
        if session.get('data') is not None:
            return redirect(url_for("search"))
        return redirect(url_for("login"))

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('data') is not None:
            return redirect(url_for("search"))
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
            # return render_template("dashboard.html", name = name + " " + fullname)
            return redirect(url_for("search"))
    return redirect(url_for("register"))

@app.route("/logout")
def logout():
    session.clear()
    logging.debug("User Logged out Successfully")
    return redirect(url_for("login"))

@app.route("/search", methods = ["GET"])
def search():
    if request.method == "GET":
        return render_template("search.html")

@app.route("/api/search", methods = ["POST"])
def api_search():
    if request.method == "POST":
        content = request.get_json(force = True)
        search_by = content["select"].strip()
        search_text = "%" + content["search_text"].strip() + "%"
        if search_by == "1":
            results = Book.query.filter(Book.author.like(search_text)).all()
        if search_by == "2":
            results = Book.query.filter(Book.isbn.like(search_text)).all()
        if search_by == "3":
            results = Book.query.filter(Book.title.like(search_text)).all()
        if search_by == "select":
            results = Book.query.filter(or_(Book.author.like(search_text), Book.isbn.like(search_text), Book.title.like(search_text)))
        if results != None:
            search_results = []
            for result in results:
                details = {"ISBN" : result.isbn, "title" : result.title}
                search_results.append(details)
            return jsonify({"success" : True, "results" : search_results})

@app.route("/book", methods = ["GET"])
def get_book():
    isbn = request.args.get('isbn')
    response = bookreads_api(isbn)
    if request.method == "GET":
        if session.get('data') is not None:
            email = session["data"]
            name = User.query.get(email).name
            review_det = Review.query.filter_by(email = email, isbn = isbn).first()
            if review_det is not None:
                rating_one = review_det.rating
                review = review_det.review
                return render_template("details.html", Name = response["name"], Author = response["author"], ISBN = response["isbn"], Year = response["year"], rating = response["average_rating"], count = response["reviews_count"], image = response["img"], button = "Edit", rating_one = rating_one, Review = review, name = name, Submit = "Edit")
            else:
                return render_template("details.html", Name = response["name"], Author = response["author"], ISBN = response["isbn"], Year = response["year"], rating = response["average_rating"], count = response["reviews_count"], image = response["img"], button = "Review", rating_one = 0, name = name, Submit = "Submit")
        return redirect(url_for("login"))

def bookreads_api(isbn):
    isbn = request.args.get("isbn")
    query = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "GeJUHhlmNf7PYbzeKEnsuw", "isbns": isbn})
    logging.debug("Goodreads call success")
    response = query.json()
    response = response['books'][0]
    book_info = Book.query.get(isbn)
    logging.debug("DB query executed successfully")
    response['name'] = book_info.title
    response['author'] = book_info.author
    response['year'] = book_info.publicationyear
    response['img'] = "http://covers.openlibrary.org/b/isbn/" + isbn + ".jpg"
    return response

@app.route("/api/review", methods = ["POST"])
def review():
    if request.method == "POST":
        email = session["data"]
        isbn = request.args.get('isbn')
        response = bookreads_api(isbn)
        review_det = Review.query.filter_by(email = email, isbn = isbn).first()
        name = User.query.get(email).name
        content = request.get_json(force = True)
        rate = content['rating'].strip()
        rev = content['review'].strip()
        if review_det is None:
            revs = Review(email, isbn, rate,rev)
            total_rating = ((float(response["average_rating"]) * int(response["reviews_count"])) + int(rate))/(int(response["reviews_count"]) + 1)
            response["average_rating"] = str(total_rating)
            response["reviews_count"] = str(int(response["reviews_count"]) + 1)
            db.session.add(revs)
            db.session.commit()
            # return render_template("details.html", Name = response["name"], Author = response["author"], ISBN = response["isbn"], Year = response["year"], rating = response["average_rating"], count = response["reviews_count"], image = response["img"], button = "Edit", rating_one = rate, Review = rev, name = name, Submit = "Edit")
            return jsonify({"success" : True, "Name" : response["name"], "Author" : response["author"], "ISBN" : response["isbn"], "Year" : response["year"], "rating" : response["average_rating"], "count" : response["reviews_count"], "image" : response["img"], "button" : "Edit", "rating_one" : rate, "Review" : rev, "name" : name, "Submit" : "Edit" })
        else:
            review_det.rating = rate
            review_det.review = rev
            total_rating = ((float(response["average_rating"]) * int(response["reviews_count"])) + int(rate))/(int(response["reviews_count"]) + 1)
            db.session.commit()
            # return render_template("details.html", Name = response["name"], Author = response["author"], ISBN = response["isbn"], Year = response["year"], rating = response["average_rating"], count = response["reviews_count"], image = response["img"], button = "Edit", rating_one = rate, Review = rev, name = name, Submit = "Edit")
            return jsonify({"success" : True, "Name" : response["name"], "Author" : response["author"], "ISBN" : response["isbn"], "Year" : response["year"], "rating" : response["average_rating"], "count" : response["reviews_count"], "image" : response["img"], "button" : "Edit", "rating_one" : rate, "Review" : rev, "name" : name, "Submit" : "Edit" })