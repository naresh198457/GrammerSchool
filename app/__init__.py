from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# creating app
app = Flask(__name__)
app.app_context().push()
app.config.from_pyfile("config.cfg")

#Creating database
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)

# login manager
login_manager = LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category = 'info'

from app import route
