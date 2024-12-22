import pandas as pd
import numpy as np
import string
import random


def find_next_pair_letters(No_questions):
    
    letters = string.ascii_uppercase

    Combos_set = []
    options_set =[]

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
        options_set.append([letters[no11]+letters[no21],
                            letters[no11]+letters[no22],
                            letters[no12]+letters[no22],
                            letters[no13]+letters[no23]])

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

        options_set.append([letters[no11]+letters[no21],
                            letters[no11]+letters[no22],
                            letters[no12]+letters[no22],
                            letters[no13]+letters[no23]])

        Combos_set.append(comb_set)
            
    return Combos_set, options_set

leters_set, option_set = find_next_pair_letters(10)
print(leters_set)
print(option_set)

# ----------------------------------------------------------------------
def same_letter_must_fit_into_both(noofquestions):

    df_start = pd.read_csv('G:\My Drive\Mishitha\GrammerSchool\datafiles\words_start.csv')
    df_end = pd.read_csv('G:\My Drive\Mishitha\GrammerSchool\datafiles\words_end.csv')

    letter_list=df_end['letter'].unique().tolist()

    word_question = []
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
        word_question.append(word1+' [?] '+word2 + '        ' + word3+' [?] '+word4)
        word_letters.append(l)

    return word_question, word_letters

words_set, letters_set = same_letter_must_fit_into_both(8)

print(words_set)
print(letters_set)




