import os

from flask import Flask, render_template,session
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

@app.route("/home", methods=["POST"])
def register():
    """Making Registration"""

    #Get form information
    username = request.form.get("username");
    password = request.form.get("password");
    email = request.form.get("email");

    db.execute("INSERT INTO users (username, password, email) VALUES(:username, :password, :email)")
