import jwt, datetime, os 
from flask import Flask, request 
from flask_mysqldb import MySQL

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the .env file (two levels up from the current file)
dotenv_path = os.path.join(current_dir, '..', '..', '.env')


server = Flask(__name__)
mysql = MySQL(server)

# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")

@server.route("/login", methods=["POST"])
def login():
  auth = request.authorization

  if not auth or not auth.username or not auth.password:
    return "Missing credentials", 401

  # check if the user exists
  cur = mysql.connection.cursor()
  result = cur.execute(
    "SELECT email, password FROM user WHERE email = %s", (auth.username,)
  )

  if result > 0:
    user_data = cur.fetchone()
    email = user_data[0]
    password = user_data[1]

    if auth.username != email or auth.password != password:
      return "Invalid credentials", 401
    else:
      return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
  else:
    return "Invalid credentials", 401
  

def createJWT(username, secret, authz):
  return jwt.encode(
    {
      "username": username,
      "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
      "iat": datetime.datetime.utcnow(),
      "admin": authz
    },
    secret,
    algorithm="HS256",
  )

@server.route("/validate", methods=["POST"])
def validate():
  token = request.headers["Authorization"]

  if not token:
    return "Missing token", 401

  try:
    encoded_jwt = token.split(" ")[1]
    decoded = jwt.decode(encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"])
    return decoded
  except:
    return "Unauthorized", 403


if __name__ == "__main__":
  server.run(host="0.0.0.0", port=5000)