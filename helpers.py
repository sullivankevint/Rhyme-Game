import requests
import json
import time
import sys

#function checks if a word is in MW dictionary and defined as offensive with (bool, bool) response
def check_dict(word):
    mw_key='?key=7d3e55d9-1c6b-4005-87da-5273335b14ee'
    mw_url = 'https://www.dictionaryapi.com/api/v3/references/collegiate/json/'

    mw_response_url = mw_url + word.lower() + mw_key
    mw_response = requests.get(mw_response_url).json()
    #responses may be empty lists or lists of suggested words in list form. if/elif is used to not produce an index error if an empty list is given
    if len(mw_response) == 0:
        return (False, False)
    elif not isinstance(mw_response[0], dict):
        return (False, False)
    if (mw_response[0]['meta']['offensive'] == True):
        return (True, True)
    else:
        return (True, False)

#function returns true for if word is one syllable
def check_one_syllable(word):
    dm_url = 'https://api.datamuse.com/words?'
    orig_word_param_prefix = 'sp='
    orig_word_param_suffix = '&qe=sp&md=s&max=1'

    orig_word_response_url = dm_url + orig_word_param_prefix + word.lower() + orig_word_param_suffix
    orig_word_response = requests.get(orig_word_response_url)
    orig_word_data = orig_word_response.json()
    if orig_word_data[0]['numSyllables'] > 1:
        return False
    else:
        return True

def get_word_list(word):
    dm_url = 'https://api.datamuse.com/words?'
    rhyme_param = 'rel_rhy='
    syllable_params = '&md=s'
    related_word_respone_url = dm_url + rhyme_param + word.lower() + syllable_params
    related_word_response = requests.get(related_word_respone_url).json()
    target_words = []
    for i, element in enumerate(related_word_response):
        progress = float(i) / len(related_word_response)
        update_progress(progress)
        is_word, is_offensive = check_dict(element['word'])
        if (element['numSyllables'] == 1) and (is_word == True) and (is_offensive == False):
            target_words.append(element['word'])

    target_words.sort()
    print('')
    return target_words
   
def update_progress(progress):
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rLoading Word List: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), round(progress*100), status)
    sys.stdout.write(text)
    sys.stdout.flush()

