from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os


# Initialize the app and database
app = Flask(__name__)
app.app_context().push()  # Ensure we are in the app context
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
# app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
# app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
# app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
# app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL')#
# app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
app.config.from_pyfile('config.cfg')


#Creating database
db = SQLAlchemy(app)
#db.init_app(app)
bcrypt=Bcrypt(app)

# login manager
login_manager = LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category = 'info'

with app.app_context():
    from . import db, app
    db.create_all()  # Create tables if they don't exist

from app import route