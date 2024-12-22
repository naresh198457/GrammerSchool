import nltk
from nltk.corpus import words
import pandas as pd
import string

# Download the words corpus
nltk.download('words')

# Get the list of words
word_list = words.words()
#print(word_list)

words = [word for word in word_list if 2<len(word)<6]
print(len(words))
#print(words)

df = pd.DataFrame(data=words, columns=['Word'])
print(df)

# I need to reduce the no of words to most common words (generally we using words). we can use the gpt model to remove the unwanted words. 


# create a df starting letter and ending letter must be same. Save them in 
dfs={}
for letter in string.ascii_lowercase:

    start_words = [word for word in words if word[0]==letter]
    end_words = [word for word in words if word[len(word)-1]==letter]
    print(start_words)
    print(end_words)
     
    dfs[f'df_{letter}'] = pd.DataFrame(columns=['start','end'])


    print(f'df_{letter}')
    print(dfs[f'df_{letter}'])
    