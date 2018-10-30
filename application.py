import os

from flask import Flask, render_template, session, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__, static_url_path='/static')

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template('index.html')

@app.route("/home",methods=["GET", "POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    #check to see if someone with this username is in database of users
    table = db.execute("SELECT * FROM users WHERE username=username AND password=password")

    if(table != None):
        return render_template('home.html', username = username)
@app.route("/success", methods=["POST"])
def success():

    #Get form information
    username = request.form.get("username")
    password = request.form.get("password")

    db.execute("INSERT INTO users (username, password) VALUES(:username, :password)",
                                {"username":username, "password":password})
    db.commit()

    return render_template('success.html')

@app.route("/register", methods=["GET", "POST"])
def register():
        return render_template('signup.html')
