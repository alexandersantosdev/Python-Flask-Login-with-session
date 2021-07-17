from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SECRET_KEY'] = 'secretkey'

db = SQLAlchemy(app)

login_manger = LoginManager()
login_manger.init_app(app)

from app import routes