import os
import hashlib
import logging
from flask import Flask, session, render_template, request, redirect, flash, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
from models import *
from create import app


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
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# logging.debug("database sessions created")

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

@app.route("/userreview", methods = ["POST"])
def user_review():
    if request.method == "POST":
        if session.get("data"):
            query = request.form.get("search_item")
            users = User.query.filter(or_(User.email.ilike(query), User.name.ilike(query))).all()
            rev = []
            for user in users:
                rev = rev + Review.query.filter_by(email= user.email).group_by(Review.email,Review.isbn).order_by(Review.time_stamp.desc()).all()
            try:
                rev[0].isbn
                return render_template("userreviews.html", rev=rev)
            except Exception:
                flash("No reviews so far","info")
                return render_template("userreviews.html", rev=rev)
        else :
            flash("Please Login First", "info")
            return redirect("/login")

@app.route("/reviewsearch", methods = ["GET"])
def review_search():
    if request.method == "GET":
        if session.get("user_email"):
            email = session.get("user_email")
            return render_template("userreview.html", email=email)
        else :
            flash("Please Login First", "info")
            return redirect("/login")

@app.route("/api/userreview", methods=["POST"])
def userReviewAPI() :

    try :

        if not request.is_json :
            return jsonify({"error" : "not a json request"}), 400

        reqData = request.get_json()
        #print(reqData)
        if "email" not in reqData :
            return jsonify({"error" : "missing email key"}), 400

        if "search" not in reqData :
            return jsonify({"error" : "missing search key"}), 400

        email = reqData.get("email")

        registered = User.query.get(email)

        if registered is None :
            return jsonify({"error": "Not a registered user"})
        #print(email)

        query = reqData.get("search")
        #print(query)

        if len(query) == 0:
            #print("rtyuicvbn")
            return jsonify({"error" : "no results found"}), 404
        #print("hello")
        users = User.query.filter(or_(User.email.ilike(query), User.name.ilike(query))).all()
        #print(users)
        rev = []
        
        for user in users:
            rev = rev + Review.query.filter_by(email=user.email).group_by(Review.email,Review.isbn).order_by(Review.time_stamp.desc()).all()
        #print(rev)
        try:

            rev[0].isbn
            
            reviews = []

            for r in rev :

                temp = {}
                temp["isbn"] = r.isbn
                temp["email"] = r.email
                temp["rating"] = r.rating
                temp["comments"] = r.review
                temp["timestamp"] = r.time_stamp
                reviews.append(temp)
                #print(reviews)
            return jsonify({"reviews" : reviews}), 200
        except Exception:
            #print(exc)
            return jsonify({"error" : "No reviews so far"}), 404
    except Exception:
        #print(exc)

        return jsonify({"error" : "Server Error"}), 500


if __name__ == "__main__" :
    app.run(debug=True)