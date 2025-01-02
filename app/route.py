from app import app
from flask import render_template, request, url_for, flash, redirect, session
import os
from flask_mail import Mail, Message
from app.models import db
from app.models import User, dailyActivity
from app.forms import RegistrationForm, LoginForm, contactForm, practiceform, commonletterquestionform, findnextletterpairform
from app.functions import same_letter_must_fit_into_both, find_next_pair_letters, create_bar_chart, create_pie_chart
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required
import pandas as pd
from datetime import datetime, timedelta


# login page
@app.route('/')
@app.route('/home',methods=['POST','GET']) # decorators: '/' route page of our website
def home():
    image_file=url_for('static',filename='profile_pics/'+current_user.image_file)
    return render_template('home.html',image_file=image_file)


# about route
@app.route("/about",methods=['GET','POST'])
def about():

    Designer_im_file=url_for('static',filename='Desiner_Pics/Naresh_BW.jpg')
    
    return render_template('about.html',Designer_im_file=Designer_im_file)
    

# Practice route
@app.route("/practice", methods = ['GET', 'POST'])
def practice():
    
    global cl_q_no, cl_a_no, df_cl
    global CL_questions_1, CL_questions_2, CL_Answers, CL_urAnswers

    # common letter variables 
    df_cl = same_letter_must_fit_into_both(7)
    cl_q_no = cl_a_no = 0
    CL_questions_1 = []
    CL_questions_2 = []
    CL_Answers = []
    CL_urAnswers = []

    global df_fnpl, fnpl_q_no, fnpl_a_no
    global FNPL_letters_1, FNPL_letters_2, FNPL_letters_3, FNPL_letters_4, FNPL_Answers, FNPL_urAnswers

    # find next pair letters varibles
    df_fnpl = find_next_pair_letters(7)
    fnpl_q_no = fnpl_a_no = 0
    FNPL_letters_1 = []
    FNPL_letters_2 = []
    FNPL_letters_3 = []
    FNPL_letters_4 = []
    FNPL_Answers = []
    FNPL_urAnswers = []

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

    global cl_q_no, cl_a_no, df_cl
    global CL_questions_1, CL_questions_2, CL_Answers, CL_urAnswers  

    if cl_q_no >= len(df_cl):

        return redirect(url_for('commonletterdashboard'))

    question_data = df_cl.iloc[cl_q_no]
    answer = question_data['answer']
    form = commonletterquestionform()
    form.options.choices = [(option, option) for option in question_data['options']]

    if form.submit.data:
        selected_option = form.options.data
        CL_questions_1.append(question_data['question_1'])
        CL_questions_2.append(question_data['question_2'])
        CL_Answers.append(question_data['answer']) 
        CL_urAnswers.append(selected_option)         

        if selected_option == answer:
            cl_a_no += 1
        cl_q_no += 1
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
    global df_fnpl, fnpl_q_no, fnpl_a_no
    global FNPL_letters_1, FNPL_letters_2, FNPL_letters_3, FNPL_letters_4, FNPL_Answers, FNPL_urAnswers

    if fnpl_q_no >= len(df_fnpl):

        return redirect(url_for('nextletterpairdashboard'))

    question_data = df_fnpl.iloc[fnpl_q_no]
    answer = question_data['answer']
    form = findnextletterpairform()
    form.options.choices = [(option, option) for option in question_data['options']]

    if form.submit.data:
        selected_option = form.options.data
        FNPL_letters_1.append(question_data['letter1'])
        FNPL_letters_2.append(question_data['letter2'])
        FNPL_letters_3.append(question_data['letter3'])
        FNPL_letters_4.append(question_data['letter4'])
        FNPL_Answers.append(question_data['answer']) 
        FNPL_urAnswers.append(selected_option)         

        if selected_option == answer:
            fnpl_a_no += 1
        fnpl_q_no += 1
        return redirect(url_for('nextletterpair'))

    return render_template(
        'nextletterpair.html',
        letter1=question_data['letter1'],
        letter2=question_data['letter2'],
        letter3=question_data['letter3'],
        letter4=question_data['letter4'],
        form=form
    )

@app.route("/nextletterpairdashboard")
def nextletterpairdashboard():
    global df_fnpl, fnpl_q_no, fnpl_a_no
    global FNPL_letters_1, FNPL_letters_2, FNPL_letters_3, FNPL_letters_4, FNPL_Answers, FNPL_urAnswers

    
    return render_template('nextletterpairdashboard.html', 
                           FNPL_letters_1=FNPL_letters_1, 
                           FNPL_letters_2=FNPL_letters_2, 
                           FNPL_letters_3=FNPL_letters_3, 
                           FNPL_letters_4=FNPL_letters_4, 
                           FNPL_Answers=FNPL_Answers, 
                           FNPL_urAnswers=FNPL_urAnswers,
                           fnpl_q_no=fnpl_q_no, 
                           fnpl_a_no=fnpl_a_no)



