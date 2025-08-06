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
def Number_seperation(No):
    No=str(No)
    if len(No)==3:
        No1=No[2]
        No2=No[1]
        No3=No[0]
    elif len(No)==2:
        No1=No[1]
        No2=No[0]
        No3=' '
    elif len(No)==1:
        No1=No[0]
        No2=' '
        No3=' '
    return No1, No2, No3

def generating_RandomNumbers(No,No1,No2):
    Numbers=[]
    for _ in range(No):
        Numbers.append(random.randint(No1,No2))
    return Numbers


# -------------------------------------------------------------------
def generate_table_sequence():
    # Choose a random multiplication table (1-12)
    table = random.randint(1, 12)
    
    # Choose a random starting point (1-12)
    start = random.randint(1, 12)
    
    # Generate sequence by going through the table
    sequence = [table * (start + i) for i in range(7)]
    
    # Ensure all numbers are below 150
    while any(num >= 150 for num in sequence):
        # If any number is too large, pick a smaller table or start earlier
        table = random.randint(1, 8)
        start = random.randint(1, 5)
        sequence = [table * (start + i) for i in range(7)]
    
    return sequence


def generate_options(answer, range_limit=8, total_options=5):
    options = set()
    options.add(answer)
    
    while len(options) < total_options:
        option = answer + random.randint(-range_limit, range_limit)
        if option != answer:
            options.add(option)
    
    options = list(options)
    random.shuffle(options)
    return options


def generate_sequence():
    # Choose a random pattern type
    pattern_type = random.choice(['increment', 'decrement', 'multiply', 'alternate'])
    
    # Generate sequence based on pattern type
    if pattern_type == 'increment':
        start = random.randint(1, 50)
        step = random.randint(2, 10)
        sequence = [start + i*step for i in range(7)]
    elif pattern_type == 'decrement':
        start = random.randint(100, 140)
        step = random.randint(2, 10)
        sequence = [start - i*step for i in range(7)]
    elif pattern_type == 'multiply':
        sequence = generate_table_sequence()
    else:  # alternate pattern
        start = random.randint(10, 30)
        sequence = [start + (5 if i%2==0 else -2) for i in range(7)]
        for i in range(1, 7):
            sequence[i] += sequence[i-1] - start
    
    # Ensure all numbers are below 150
    sequence = [num for num in sequence if num < 150]
    
    # If sequence is too short due to filtering, generate a simple increment one
    if len(sequence) < 7:
        start = random.randint(1, 20)
        step = random.randint(3, 7)
        sequence = [start + i*step for i in range(7)]

    new_sequence = sequence[:7]
    removing_pos_number = random.randint(0, 4)
    answer = new_sequence[removing_pos_number]
    sequence_str = [str(new_sequence[i]) if i!= removing_pos_number else '__' for i in range(len(new_sequence))]
    sequence_str_str = " &emsp; &emsp; ".join(sequence_str)

    question_option = generate_options(answer, range_limit=8, total_options=5)
    
    return sequence_str_str, answer, question_option

def create_list_numberquestion(no_quetions):

    df=pd.DataFrame(columns=['sequence', 'answer', 'options'])
    df['options'] = None
    df = df.astype({'options': 'object'})
    for i in range(no_quetions):

        sequ_str, answer, question_options = generate_sequence()
        df.at[i, 'sequence'] = sequ_str
        df.at[i, 'answer'] = answer
        df.at[i, 'options'] = set(question_options)

    return df
        


# -------------------------------------------------------------------