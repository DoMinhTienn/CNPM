from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key="cdcdjsiuh343445*&%%&**HH>>>OJY&&&(("
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1951050100@localhost/ttth?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db =SQLAlchemy(app= app)