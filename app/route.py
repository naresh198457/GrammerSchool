from app import app
from flask import render_template, request, url_for, flash, redirect, session
from app.forms import practiceform, commonletterquestionform, findnextletterpairform, Arithmeticsform, BTForm, identifynextnumberform
from app.functions import same_letter_must_fit_into_both, find_next_pair_letters, Number_seperation, generating_RandomNumbers
from app.functions import generate_sequence, create_list_numberquestion
import random
import pandas as pd

# login page
@app.route('/')
@app.route('/home',methods=['POST','GET']) # decorators: '/' route page of our website
def home():
     # Brain teaser
    
    image_file=url_for('static',filename='profile_pics/default.jpg')
    return render_template('home.html',image_file=image_file)    

# Practice route
@app.route("/practice", methods = ['GET', 'POST'])
def practice():
    
    global cl_q_no, cl_a_no, df_cl
    global CL_questions_1, CL_questions_2, CL_Answers, CL_urAnswers

    # common letter variables 
    df_cl = same_letter_must_fit_into_both(10)
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

    # arthimetic 
    global Add_No_1, Add_No_2, Sub_No_1, Sub_No_2, Mul_No_1, Mul_No_2
    global Add_corrected_ans,Sub_corrected_ans,Mul_corrected_ans
    global question_no
    global Arith_Ans,number1, number2

    Add_No_1=generating_RandomNumbers(25,101,500)
    Add_No_2=generating_RandomNumbers(25,11,99)
    Sub_No_1=generating_RandomNumbers(25,11,99)
    Sub_No_2=generating_RandomNumbers(25,11,55)
    Mul_No_1=generating_RandomNumbers(25,0,10)
    Mul_No_2=[2,3,4,5,10]*6
    Mul_No_2=random.sample(Mul_No_2,len(Mul_No_2))
    question_no =0 

    Add_corrected_ans=0
    Sub_corrected_ans=0
    Mul_corrected_ans=0
    question_no=0
    Arith_Ans=[]
    number1=[]
    number2=[]    

    # identify the numbers sequence
    global in_q_no, in_a_no, df_in
    global IN_questions, IN_Answers, IN_urAnswers  
    df_in = create_list_numberquestion(10)
    in_q_no = 0
    in_a_no = 0   
    IN_questions = []
    IN_Answers = []
    IN_urAnswers =[]

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
        
        elif 'submit_button_4' in request.form:
            print('Arthematics')
            return redirect(url_for('Arithmetics'))

    return render_template('practice.html', form=form)


@app.route("/commonletter", methods=['GET', 'POST'])
def commonletter():

    global cl_q_no, cl_a_no, df_cl
    global CL_questions_1, CL_questions_2, CL_Answers, CL_urAnswers  

    if cl_q_no >= len(df_cl):

        return redirect(url_for('commonletterdashboard'))

    question_data = df_cl.iloc[cl_q_no]
    print(question_data)
    answer = question_data['answer']
    print(answer)
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
        form=form,
        cl_q_no=cl_q_no, 
        cl_q = len(df_cl)
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

    global in_q_no, in_a_no, df_in
    global IN_questions, IN_Answers, IN_urAnswers  

    if in_q_no >= len(df_in):
        
        return redirect(url_for('identifynumbersdashboard'))
    
    question = df_in.iloc[in_q_no]
    answer = question['answer']
    question_option = question['options']
    # print(f"Question: {question}, Answer: {answer}, Options: {question_option}")
    
    form = identifynextnumberform()
    form.options.choices = [(option, option) for option in question_option]

    if form.submit.data:
        selected_option = form.options.data
        # print(f"Selected Option: {selected_option}")

        print("Answer field from df:", answer, type(answer))
        
        # print(f"Question: {question['sequence']}")
        # print(f"selected option: {selected_option}")
        IN_questions.append(question['sequence'].replace('&emsp; &emsp;', ' '))
        IN_Answers.append(int(answer)) 
        IN_urAnswers.append(int(selected_option))   
        print(IN_Answers) 
        print(IN_urAnswers)


        if int(selected_option) == int(answer):
            print("Correct answer!")
            in_a_no += 1
        print(f"Current Question Number: {in_q_no}, Correct Answers: {in_a_no}")
        in_q_no += 1
        return redirect(url_for('identifynextnumber'))

    return render_template('identifynextnumber.html', 
                           form= form,
                           answer=answer, 
                           question=question['sequence'], 
                           question_option=question_option,
                           in_q_no=in_q_no,
                           in_a_no=in_a_no,
                           in_q = len(df_in))

@app.route("/identifynumbersdashboard")
def identifynumbersdashboard():
    global in_q_no, in_a_no, df_in
    global IN_questions, IN_Answers, IN_urAnswers  

    IN_Answers = [int(ans) for ans in IN_Answers]
    IN_urAnswers = [int(ans) for ans in IN_urAnswers]
    IN_questions = [str(q) for q in IN_questions]

    return render_template('identifynumbersdashboard.html', 
                           IN_questions=IN_questions,
                           IN_Answers=IN_Answers,
                           IN_urAnswers=IN_urAnswers,
                           in_a_no=in_a_no,
                           in_q_no=in_q_no)

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
        form=form, 
        fnpl_q_no=fnpl_q_no,
        fnpl_q = len(df_fnpl)
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

# Arthemetic test
Symbols=['+','+','+','+','+','+','+',
         '-','-','-','-','-','-','-',
         'x','x','x','x','x','x','x']

@app.route("/Arithmetics",methods=['POST','GET'])
def Arithmetics():
    global no1, no2, question_no
    global Add_corrected_ans, Sub_corrected_ans, Mul_corrected_ans, Symbols
    global Arith_Ans, number1, number2
    
    symb=Symbols[question_no]

    # selecting the correct numbers for the 
    if question_no<7:
        print('ADDition')
        Numbers_1=Add_No_1[question_no]
        Numbers_2=Add_No_2[question_no]
        if Numbers_2>Numbers_1:
            Numbers_1=Add_No_2[question_no]
            Numbers_2=Add_No_1[question_no]
        Ans=Numbers_1+Numbers_2

    elif question_no<14:
        print('Substraction')
        Numbers_1=Sub_No_1[question_no]
        Numbers_2=Sub_No_2[question_no]
        if Numbers_2>Numbers_1:
            Numbers_1=Sub_No_2[question_no]
            Numbers_2=Sub_No_1[question_no]
        Ans=Numbers_1-Numbers_2
    
    else: 
        Numbers_1=Mul_No_1[question_no]
        Numbers_2=Mul_No_2[question_no]
        Ans=Numbers_1*Numbers_2

    # Once it reaches to the 20 questions
    if question_no==20:
        return redirect(url_for('Arithmetics_dashBoard'))
    
    # calling the form
    No1_1, No2_1, No3_1=Number_seperation(Numbers_1)
    No1_2, No2_2, No3_2=Number_seperation(Numbers_2)
    form=Arithmeticsform(No_1_1s=No1_1,
                         No_1_10s=No2_1,
                         No_1_100s=No3_1,
                         No_2_1s=No1_2,
                         No_2_10s=No2_2,
                         No_2_100s=No3_2,
                         Symbol=symb)

    if form.validate_on_submit():
        if form.Next_Button.data:
            number3=form.No_3_100s.data+form.No_3_10s.data+form.No_3_1s.data
            Arith_Ans.append(int(number3))
            number1.append(Numbers_1)
            number2.append(Numbers_2)
            if int(number3)==Ans:
                if question_no<7:
                    Add_corrected_ans=Add_corrected_ans+1
                    #print(Add_corrected_ans)
                elif question_no<14:
                    Sub_corrected_ans+=1
                    #print(Sub_corrected_ans)
                else: 
                    Mul_corrected_ans+=1 
            #print(question_no,Numbers_1,symb,Numbers_2,number3,Ans) 
            question_no=question_no+1
            return redirect(url_for('Arithmetics'))

    return render_template('Arithmetics.html', form=form, question_no=question_no)

# Arithmetics dashBoard
@app.route("/Arithmetics_dashBoard",methods=['POST','GET'])
def Arithmetics_dashBoard():

    return render_template('Arithmetics_dashBoard.html',
                           Add_corrected_ans=Add_corrected_ans,
                           Sub_corrected_ans=Sub_corrected_ans,
                           Mul_corrected_ans=Mul_corrected_ans,
                           number2=number2,
                           number1=number1,
                           Arith_Ans=Arith_Ans,
                           Symbol=Symbols)

# Brainteaser practice
BT_Data=pd.read_csv('datafiles/FunnyQuestions.csv')
BT_Data=BT_Data.sample(frac=1).reset_index(drop=True) 
BT_Ques_No=0
BT_ON=0
BT_NextON=0

@app.route("/Brain Teaser",methods=['POST','GET'])
def BrainTeaser():
    global BT_Data
    global BT_Ques_No
    global BT_ON
    global BT_NextON
    
    form=BTForm(BT_Question=BT_Data.loc[BT_Ques_No,'Question'],BT_Answer=BT_Data.loc[BT_Ques_No,'Ans'])

    if form.validate_on_submit():
        if form.BT_Ans_Rev_Button.data:
            BT_ON=1
            BT_NextON=1
        if form.BT_Next.data:
            BT_ON=0
            BT_Ques_No+=1
            BT_NextON=0

            if BT_Ques_No>6:
                BT_Ques_No=0
                BT_Data=BT_Data.sample(frac=1).reset_index(drop=True)
                return redirect(url_for('home'))
        return redirect(url_for('BrainTeaser'))
    return render_template('BrainTeaser.html', form=form,BT_ON=BT_ON,BT_NextON=BT_NextON)