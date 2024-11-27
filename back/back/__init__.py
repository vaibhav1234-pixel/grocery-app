from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_object(__name__)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "groceryapp24@gmail.com"
app.config["MAIL_PASSWORD"] = "esum xoac ouyo efmo"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail = Mail(app)

app.config[
    "JWT_SECRET_KEY"
] = "your_jwt_secret_key"  # Change this to a secure, random key in production

app.config["SECRET_KEY"] = "vaibhavmishra"
SECURITY_PASSWORD_HASH = "bcrypt"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///grocery.db"
app.config["SECURITY_PASSWORD_SALT"] = "thisisasecretsalt"

cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
from back import routes
