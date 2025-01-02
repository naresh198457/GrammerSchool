import pandas as pd
import numpy as np
import string
import random
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from io import BytesIO
import base64


def find_next_pair_letters(No_questions):
    
    letters = string.ascii_uppercase

    Combos_set = []
    options_set =[]
    df = pd.DataFrame(columns=['letter1', 'letter2', 'letter3', 'letter4', 'answer', 'options'])
    df['options'] = None
    df = df.astype({'options': 'object'})

    # linear increament
    for i in range(round(No_questions*0.7)):
        No1 = random.randint(0, 20)
        No2 = random.randint(5, 26)
        
        inc = random.randint(1,4)

        while No1+6*inc>25:
            No1 = random.randint(0,20)
        
        while No2-6*inc<0:
            No2 = random.randint(5,25)
        
        comb_set =[]
        for j in range(1,6):
            no11 = No1+j*inc
            no21 = No2-j*inc

            #print(No1, no11, No2, no21)
            Comb = letters[no11]+letters[no21]

            comb_set.append(Comb)
        
        Combos_set.append(comb_set)
        no12 = no11+1
        no13 = no11+4
        if no12>25: 
            no12=no11-3
        if no13>25: 
            no13=no11-10
        
        no22 = no21-1
        no23 = no21-4
        if no22<1: 
            no22=no21+3
        if no23<1: 
            no23=no21+10

        #print(no22, no23, no21)
        options = [letters[no11]+letters[no21],
                   letters[no11]+letters[no22],
                   letters[no12]+letters[no22],
                   letters[no13]+letters[no23]]
        random.shuffle(options)
        options_set.append(options)

    # non linear increament
    NonLin = [5,4,3,2,1]
    for i in range(No_questions-round(No_questions*0.7)):

        No1 = random.randint(0, 20)
        No2 = random.randint(5, 26)

        while No1+sum(NonLin)+1>26:
            No1 = random.randint(0,20)
        
        while No2-sum(NonLin)-1<0:
            No2 = random.randint(5,26)
        
        comb_set = []
        for j in range(5):
            no11 = No1+sum(NonLin[0:j])+1
            no21 = No2-sum(NonLin[0:j])-1
            Comb = letters[No1+sum(NonLin[0:j])+1]+letters[No2-sum(NonLin[0:j])-1]
            comb_set.append(Comb)

        no12 = no11+1
        no13 = no11+4
        if no12>25: 
            no12=no11-3
        if no13>25: 
            no13=no11-10
        
        no22 = no21-1
        no23 = no21-4
        if no22<1: 
            no22=no21+3
        if no23<25: 
            no23=no21+10

        options = [letters[no11]+letters[no21],
                   letters[no11]+letters[no22],
                   letters[no12]+letters[no22],
                   letters[no13]+letters[no23]]
        random.shuffle(options)
        options_set.append(options)

        Combos_set.append(comb_set)

    for i in range(No_questions):
        df.loc[i,'letter1'] = Combos_set[i][0]
        df.loc[i,'letter2'] = Combos_set[i][1]
        df.loc[i,'letter3'] = Combos_set[i][2]
        df.loc[i,'letter4'] = Combos_set[i][3]
        df.loc[i,'answer'] = Combos_set[i][4]
        df.at[i,'options'] = options_set[i]#random.shuffle(options_set[i])
            
    return df


# ----------------------------------------------------------------------
def same_letter_must_fit_into_both(noofquestions):

    df = pd.DataFrame(columns=['question', 'answer', 'options'])

    df_start = pd.read_csv('datafiles/words_start.csv')
    df_end = pd.read_csv(r'datafiles/words_end.csv')

    letter_list=df_end['letter'].unique().tolist()

    word_question1 = []
    word_question2 = []
    word_letters = []

    letters = random.sample(letter_list,noofquestions)

    for l in letters:
        df_st = df_start.loc[df_start['letter']==l,'words'].tolist()
        df_st_list = random.sample(df_st,2)

        df_en = df_end.loc[df_end['letter']==l,'words'].tolist()
        df_en_list = random.sample(df_en,2)

        word1 = df_en_list[0][:-1]
        word2 = df_st_list[0][1:]
        word3 = df_en_list[1][:-1]
        word4 = df_st_list[1][1:]
        word_question1.append(word1+' [?] '+word2)
        word_question2.append(word3+' [?] '+word4)
        word_letters.append(l)

    df['question_1'] = word_question1
    df['question_2'] = word_question2
    df['answer'] = word_letters
    df['options'] = None
    df = df.astype({'options': 'object'})

    common = ['e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'l', 'd', 'c', 'm', 'f', 'k', 'b']
    for i in range(len(word_letters)):
        if word_letters[i] not in common:
            option_list = random.sample(common, 4)
        else: 
            updated_common = [x for x in common if x != word_letters[i]]
            option_list = random.sample(updated_common, 4)
            # option_list = random.sample(common.remove(letters_set[i]),4)
        option_list.append(word_letters[i])
        random.shuffle(option_list)
        df.at[i,'options']=option_list
        # df.loc[i,'option_b']=option_list[1]
        # df.loc[i,'option_c']=option_list[2]
        # df.loc[i,'option_d']=option_list[3]
        # df.loc[i,'option_e']=option_list[4]

    return df

# ---------------------------------------------------------------------------------------
def create_bar_chart(filtered_df):
    # Filter last 30 days
    start_date = datetime.now() - timedelta(days=30)
    last_30_days = filtered_df[filtered_df["date_test"] >= start_date]

    # Count test types per day
    bar_data = last_30_days.groupby([last_30_days["date_test"].dt.date, "testType"]).size().unstack(fill_value=0)

    # Plot bar chart
    plt.figure(figsize=(10, 6))
    bar_data.plot(kind="bar", stacked=True, ax=plt.gca())
    plt.title("Test Types Used Per Day (Last 30 Days)")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.tight_layout()

    # Save to buffer
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def create_pie_chart(filtered_df):
    # Calculate total correct answers
    correct_answers = filtered_df["correctAns"].sum()
    incorrect_answers = (filtered_df["noQuestion"] - filtered_df["correctAns"]).sum()

    # Data for pie chart
    pie_data = [correct_answers, incorrect_answers]
    labels = ["Correct Answers", "Incorrect Answers"]
    colors = ["#4CAF50", "#F44336"]

    # Plot pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(pie_data, labels=labels, autopct="%1.1f%%", colors=colors, startangle=90)
    plt.title("Percentage of Correct Answers")
    plt.tight_layout()

    # Save to buffer
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")
