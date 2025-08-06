from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin
from google.oauth2.service_account import Credentials
import os
import gspread

# Google Sheets setup
def get_google_login_sheet():
    scopes =[
        "https://www.googleapis.com/auth/spreadsheets"
    ]
    creds = Credentials.from_service_account_file("Credentials.json", scopes=scopes)
    client = gspread.authorize(creds)

    sheet_id = os.getenv('SHEET_ID')
    sheet = client.open_by_key(sheet_id)
    return sheet

@login_manager.user_loader
def load_user(user_id):
    sheet = get_google_login_sheet()
    users = sheet.get_all_records()
    for user in users:
        if user['id'] == int(user_id):
            return user
    return None

# Example of a user-like class for Flask-Login
class User:
    def __init__(self, id, username, password, firstname, lastname):
        self.id = id
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
    

class dailyActivity(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(40),db.ForeignKey('user.username'),nullable=False)
    date_test=db.Column(db.DateTime,nullable=False, default=datetime.utcnow())
    testType=db.Column(db.String(20),nullable=False)
    noQuestion=db.Column(db.Integer, nullable=False)
    correctAns=db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"dailyActivity('{self.date_test}','{self.username}','{self.correctAns}')"