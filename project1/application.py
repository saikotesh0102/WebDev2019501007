import os
import hashlib

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
from models import User
from create import *

# app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.app_context()
# db.init_app(app)
# db.create_all()

@app.route("/", methods = ['GET', 'POST'])
@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("main.html")
    elif request.method == "POST":
        email = request.form.get('email')
        pwd = request.form.get('password')
        password = hashlib.md5(pwd.encode()).hexdigest()
        user = User.query.get(email)
        if user is not None:
            if email == user.email and password == user.password:
                name = "Thank You for Logging In"
                return render_template("dashboard.html", name = name)
        return redirect(url_for("register"))

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("registration.html")
    elif request.method == 'POST':
        # session["data"] = []
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        name = fname + " " + lname
        email = request.form.get('email')
        pwd = request.form.get('password')
        password = hashlib.md5(pwd.encode()).hexdigest()
        repwd = request.form.get('repassword')
        repassword = hashlib.md5(repwd.encode()).hexdigest()
        if password == repassword:
            # session["data"].append(name)
            # session["data"].append(email)
            # session["data"].append(password)
            user = User(email, name, password)
            try:
                db.session.add(user)
            except:
                name = "Registration Unsuccessful. Please Register Again"
                return render_template("registration.html", name = name)
            db.session.commit()
            return redirect(url_for("login"))
        else:
            name = "Entered Passwords Do Not Match. Please Register Again"
            return render_template("registration.html", name = name)

@app.route("/profile", methods = ['GET', 'POST'])
def profile():
    return render_template("profile.html")

@app.route("/admin")
def admin():
    users = User.query.order_by("timestamp").all()
    return render_template("admin.html", users = users)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")