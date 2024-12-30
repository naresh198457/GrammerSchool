from app import app
from flask import render_template, request, url_for, flash, redirect, session
import os
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from app.models import db
from app.models import User, dailyActivity
from app.forms import RegistrationForm, LoginForm, contactForm, practiceform, commonletterquestionform
from app.functions import same_letter_must_fit_into_both, find_next_pair_letters
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
    

# Practice route
@app.route("/practice", methods = ['GET', 'POST'])
def practice():
    
    global cl_q_no, cl_a_no, df
    global CL_questions_1, CL_questions_2, CL_Answers, CL_urAnswers

    # common letter variables 
    df = same_letter_must_fit_into_both(7)
    cl_q_no = cl_a_no = 0
    CL_questions_1 = []
    CL_questions_2 = []
    CL_Answers = []
    CL_urAnswers = []

    form = practiceform()


    if request.method == 'POST':
        if 'submit_button_1' in request.form:
            print('Common letter page is pressed.')
            return redirect(url_for('commonletter'))
        elif 'submit_button_2' in request.form:
            print('identify the next number is pressed.')
            return redirect(url_for('identifynextnumber'))
        
        elif 'submit_button_3' in request.form:
            print('Next letter pair')
            return redirect(url_for('nextletterpair'))

    return render_template('practice.html', form=form)


@app.route("/commonletter", methods=['GET', 'POST'])
def commonletter():

    global cl_q_no, cl_a_no, df
    global CL_questions_1, CL_questions_2, CL_Answers, CL_urAnswers  

    print(f"Current question index: {cl_q_no}")

    if cl_q_no >= len(df):
        #cl_q_no = 0
        print("All questions completed, redirecting to dashboard.")
        print(CL_questions_1)
        print(CL_Answers)
        print(CL_urAnswers)
        Activity=dailyActivity(username=current_user.username,
                               testType='Arithmetic',
                               noQuestion=cl_q_no,
                               correctAns=cl_a_no)
                
        db.session.add(Activity)
        db.session.commit()
        return redirect(url_for('commonletterdashboard'))

    question_data = df.iloc[cl_q_no]
    answer = question_data['answer']
    print(question_data['question_1'], question_data['question_2'])
    print('Answer: ', question_data['answer'])
    form = commonletterquestionform()
    form.options.choices = [(option, option) for option in question_data['options']]

    if form.submit.data:
        print('next is pressed')
        selected_option = form.options.data
        print(f"User selected: {selected_option}, Correct answer: {question_data['answer']}")
        CL_questions_1.append(question_data['question_1'])
        CL_questions_2.append(question_data['question_2'])
        CL_Answers.append(question_data['answer']) 
        CL_urAnswers.append(selected_option)         

        if selected_option == answer:
            cl_a_no += 1
        cl_q_no += 1
        print(f"Updated score: {cl_a_no}, Next question: {cl_q_no}")
        return redirect(url_for('commonletter'))

    return render_template(
        'commonletter.html',
        question1=question_data['question_1'],
        question2=question_data['question_2'],
        form=form
    )


@app.route("/commonletterdashboard")
def commonletterdashboard():
    global CL_questions_1, CL_questions_2, CL_Answers, CL_urAnswers  
    global cl_q_no, cl_a_no

    cl_answers = [CL_questions_1[i].replace(' [?] ', CL_Answers[i]+', '+CL_Answers[i])+', '+ CL_questions_2[i].replace(' [?] ', CL_Answers[i]+', '+CL_Answers[i]) for i in range(cl_q_no)]
    cl_uranswers = [CL_questions_1[i].replace(' [?] ', CL_urAnswers[i]+', '+CL_urAnswers[i])+', '+ CL_questions_2[i].replace(' [?] ', CL_urAnswers[i]+', '+CL_urAnswers[i]) for i in range(cl_q_no)]
    return render_template('commonletterdashboard.html', 
                           CL_questions_1=CL_questions_1, 
                           CL_questions_2=CL_questions_2, 
                           CL_Answers=CL_Answers, 
                           CL_urAnswers=CL_urAnswers,
                           cl_answers=cl_answers,
                           cl_uranswers=cl_uranswers,
                           cl_q_no=cl_q_no, 
                           cl_a_no=cl_a_no)


@app.route("/identifynextnumber", methods = ['GET', 'POST'])
def identifynextnumber():
    return render_template('identifynextnumber.html')

@app.route("/nextletterpair", methods = ['GET', 'POST'])
def nextletterpair():
    return render_template('nextletterpair.html')

