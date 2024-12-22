from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_results.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User model to store user data
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    results = db.relationship('TestResult', backref='user', lazy=True)

# TestResult model to store test scores
class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    test_type = db.Column(db.String(20), nullable=False)  # 'verbal' or 'non-verbal'
    score = db.Column(db.Integer, nullable=False)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return "Login failed"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        results = TestResult.query.filter_by(user_id=user_id).all()
        verbal_scores = [result.score for result in results if result.test_type == 'verbal']
        non_verbal_scores = [result.score for result in results if result.test_type == 'non-verbal']
        return render_template('dashboard.html', verbal_scores=json.dumps(verbal_scores), non_verbal_scores=json.dumps(non_verbal_scores))
    return redirect(url_for('login'))

@app.route('/verbal_test', methods=['GET', 'POST'])
def verbal_test():
    if 'user_id' in session:
        if request.method == 'POST':
            # Save the verbal test score to the database
            score = int(request.form['score'])
            test_result = TestResult(user_id=session['user_id'], test_type='verbal', score=score)
            db.session.add(test_result)
            db.session.commit()
            return redirect(url_for('dashboard'))
        
        questions = [{'question': f'Verbal Question {i+1}', 'options': ['A', 'B', 'C', 'D']} for i in range(60)]
        return render_template('verbal_test.html', questions=questions)
    return redirect(url_for('login'))

@app.route('/non_verbal_test', methods=['GET', 'POST'])
def non_verbal_test():
    if 'user_id' in session:
        if request.method == 'POST':
            # Save the non-verbal test score to the database
            score = int(request.form['score'])
            test_result = TestResult(user_id=session['user_id'], test_type='non-verbal', score=score)
            db.session.add(test_result)
            db.session.commit()
            return redirect(url_for('dashboard'))

        questions = [{'question': f'Non-Verbal Question {i+1}', 'options': ['A', 'B', 'C', 'D']} for i in range(60)]
        return render_template('non_verbal_test.html', questions=questions)
    return redirect(url_for('login'))

@app.route('/practice')
def practice():
    if 'user_id' in session:
        practice_sessions = [{'session': f'Practice Session {i+1}', 'questions': [{'question': f'Practice Question {j+1}', 'options': ['A', 'B', 'C', 'D']} for j in range(20)]} for i in range(12)]
        return render_template('practice.html', practice_sessions=practice_sessions)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates the SQLite database with the User and TestResult tables
    app.run(debug=True)
