"""
Create the back end for a game that enters a one syllable word, checks if it's in the Merriam Webster dictionary
then populates a list of all other one syllable words that rhyme that the user must fill out. Rhyming data is from
Datamuse API

"""

import time
import pandas as pd
import helpers
import _thread
from ast import literal_eval
import warnings

warnings.filterwarnings('ignore')

#function to create a timer to give 2 minutes to answer
def countdown():
        global timeout
        time.sleep(120)
        timeout = True


word_choice = input('Please enter a one syllable word to rhyme: ')
is_word, is_offensive = helpers.check_dict(word_choice)
timeout = False



if  is_word == False:
    print('%s must be defined in the dictionary.' % word_choice.capitalize())
else:
    if helpers.check_one_syllable(word_choice) == False:
        print('Your word must be one syllable.')
    else:
        target_words = helpers.get_word_list(word_choice)
        
        
        #created this block with answers for 'frame' to use for faster debugging previous declaration of target_words and this are incompatible
        #with open('answers.txt', 'r') as f:
        #    target_words = f.read()
        #target_words = literal_eval(target_words)

        words = pd.DataFrame(target_words)
        
        words.columns = ['answers']
        words['guess'] = ''
        words['is_guessed'] = False
        win_status = False
        while True:
            timer = _thread.start_new_thread(countdown, ())
            for i in range(len(words.answers)):
                print(str(i+1) + ': ', end ='')
                print(words.guess[i])
            word_guess = input('Guess the one syllable words that rhyme: ')
            if word_guess in words.answers.values:
                index = words.answers.tolist().index(word_guess.lower())
            else:
                index = -1
            print('\r', end='')
            if index >= 0:
                words.guess[index] = word_guess
                words.is_guessed[index] = True            
            if words.is_guessed.all():
                break
            if timeout == True:
                break
        if(win_status == True):
            for i in range(len(words.answers)):
                print(str(i+1) + ': ', end ='')
                print(words.guess[i])
            print('Congratulations! You got all the words')
        else:
            print('Too bad! You ran out of time!')
