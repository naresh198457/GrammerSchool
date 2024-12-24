# you need to run this code for first time to create a database. 

from app import db, app

with app.app_context():
    db.create_all()