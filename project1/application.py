import os
import logging

from flask import Flask, session, render_template, request, redirect
from flask_session import Session
import hashlib
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# # Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# # Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))

@app.route("/", methods = ['GET', 'POST'])
@app.route("/login", methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("main.html")

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("registration.html")
    elif request.method == 'POST':
        session["data"] = []
        fname = request.form.get('firstname')
        lname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')
        password = hashlib.md5(password.encode()).hexdigest()
        session["data"].append(fname)
        session["data"].append(lname)
        session["data"].append(email)
        session["data"].append(password)
        return render_template("profile.html",notesdata = session["data"])

@app.route("/profile", methods = ['GET', 'POST'])
def profile():
    return render_template("profile.html")