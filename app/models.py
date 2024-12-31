from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create Model
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(40),unique=True,nullable=False)
    email=db.Column(db.String(80),nullable=False)
    image_file=db.Column(db.String(20),nullable=False, default='default.jpg')
    firstname=db.Column(db.String(30),nullable=False)
    lastname=db.Column(db.String(30),nullable=False)
    password=db.Column(db.String(60),nullable=False)
    activties=db.relationship('dailyActivity',backref='name',lazy=True)   
    
    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

class dailyActivity(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(40),db.ForeignKey('user.username'),nullable=False)
    date_test=db.Column(db.DateTime,nullable=False, default=datetime.utcnow())
    testType=db.Column(db.String(20),nullable=False)
    noQuestion=db.Column(db.Integer, nullable=False)
    correctAns=db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"dailyActivity('{self.date_test}','{self.username}','{self.correctAns}')"