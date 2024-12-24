from app import app
from flask import render_template, request, url_for, flash, redirect
import os
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from app.models import db
from app.models import User, dailyActivity
from app.forms import RegistrationForm, LoginForm, contactForm
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required


mail=Mail(app)
s=URLSafeTimedSerializer('Thisissecret!')

# login page
@app.route('/')
@app.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            #flash(f'{user.firstname} have been logged in!','success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. please check the username and password','danger')
            print('Login unsucessful')
    return render_template('login.html', title='Login',form=form)

# register page
@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # adding the new data to the database
        hash_password=generate_password_hash(password=form.password.data).decode('utf-8')
        user=User(username=form.username.data,
                  email=form.email.data,
                  firstname=form.firstname.data,
                  lastname=form.lastname.data,
                  password=hash_password)
        db.session.add(user)
        db.session.commit()

        # send the conformation email to the user
        email=form.email.data

        msg=Message('Home Work -- registeration email',
                    recipients=[email],
                    sender='naresh.sampara@gmail.com',
                    html=render_template('Email_coformation.html',
                                         UserLastName=form.lastname.data.capitalize(),
                                         UserFirstName=form.firstname.data.capitalize(),
                                         Username=form.username.data,
                                         UserEmail=form.email.data))
        mail.send(msg)
        
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('login'))
    return render_template('register.html', title='register',form=form,)

# home page
@app.route('/home',methods=['POST','GET']) # decorators: '/' route page of our website
@login_required
def home():
    image_file=url_for('static',filename='profile_pics/'+current_user.image_file)
    return render_template('home.html',image_file=image_file)

# account page 
@app.route('/account')
@login_required
def account():
    image_file=url_for('static',filename='profile_pics/'+current_user.image_file)

    # get the data from the DB
    
    return render_template('account.html',image_file=image_file)

# Logout route
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

# about route
@app.route("/about",methods=['GET','POST'])
def about():
    form=contactForm()
    Designer_im_file=url_for('static',filename='Desiner_Pics/Naresh_BW.jpg')
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('about.html', form=form)
        else:
            msg=Message(form.Subject.data,
                        sender='naresh.sampara@gmail.com',
                        recipients=['dr.sampara@gmail.com'],
                        html=render_template('Contact_Enquire.html',
                                         UserName=form.Name.data.capitalize(),
                                         UserEmail=form.Email.data,
                                         UserMessage=form.Message.data))
            mail.send(msg)
            return render_template('about.html',success=True)
    elif request.method == 'GET':
        
        return render_template('about.html',Designer_im_file=Designer_im_file,form=form)