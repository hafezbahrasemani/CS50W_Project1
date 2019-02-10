import os

from flask import Flask
from flask_bcrypt import Bcrypt

from flask import Flask, render_template, session, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__, static_url_path='/static')
bcrypt = Bcrypt(app)

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


@app.route("/", methods=["GET","POST"])
def index():
    return render_template('index.html')

@app.route("/login",methods=["GET", "POST"])
def login():

    Username = request.form["username"]
    Password = request.form["password"]

    # check to see if someone with this username is in database of users
    table = db.execute("SELECT * FROM users WHERE username=Username AND password=Password")

    if(table != None):
       return render_template('home.html', username = Username)

    # query = db.query(User).filter(User.username.in_([Username]), User.password.in_([Password]) )
    # result = query.first()
    #
    # if(result):
    #     return render_template('success.html')
    else:
        flash('Wrong Password')
        return render_template('index.html')

@app.route("/success", methods=["POST"])
def success():

    #Get form information
    username = request.form.get("username")
    password = request.form.get("password")

    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    db.execute("INSERT INTO users (username, password) VALUES(:username, :password)",
                                {"username":username, "password":pw_hash})
    db.commit()

    return render_template('success.html')

@app.route("/register", methods=["GET", "POST"])
def register():
        return render_template('signup.html')
