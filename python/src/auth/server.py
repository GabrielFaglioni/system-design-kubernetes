import jwt, datetime, os 
from flask import Flask, request 
from flask_mysqldb import MySQL
from dotenv import load_dotenv

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the .env file (two levels up from the current file)
dotenv_path = os.path.join(current_dir, '..', '..', '.env')

# Load environment variables from .env file
load_dotenv()

server = Flask(__name__)
mysql = MySQL(server)

# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")

@server.route("/login", methods=["POST"])
def login():
  auth = request.authorization

  if not auth or not auth.username or not auth.password:
    return "missing credentials", 401

  # check if the user exists
  cur = mysql.connection.cursor()
  result = cur.execute(
    "SELECT email, password FROM users WHERE email = %s", (auth.username,)
  )

  if result > 0:
    user_data = cur.fetchone()
    email = user_data[0]
    password = user_data[1]

    if auth.username != email or auth.password != password:
      return "invalid credentials", 401
    else:
      return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
  else:
    return "invalid credentials", 401