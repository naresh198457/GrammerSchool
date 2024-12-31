from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Initialize the app and database
app = Flask(__name__)
app.config.from_pyfile("config.cfg")  # Make sure this points to the correct config file
app.app_context().push()  # Ensure we are in the app context

#Creating database
db = SQLAlchemy(app)
#db.init_app(app)
bcrypt=Bcrypt(app)

# login manager
login_manager = LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category = 'info'

from app import route
