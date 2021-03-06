from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.getenv("SECRET_KEY"))
app.config['SQLALCHEMY_DATABASE_URI']=str(os.getenv("DATABASE_URI"))
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from application import routes

