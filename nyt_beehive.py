from english_words import english_words_lower_alpha_set
import matplotlib.pyplot as plt
from collections import OrderedDict
import numpy as np
import sys

#get all of the words in the english dictionary
def get_dictionary_word_list():
    new_word_list = []
    word_list = english_words_lower_alpha_set
    for word in word_list:
        if '.' not in word:
            new_word_list.append(word)
    return sorted(new_word_list)

#update word list to be just the words it could be given letters and what MUST be in there
def words_could_be(word_list, must_letter, other_letters):
    #input unknown letters of word as ? to tell program you don't know

    #only get words long enough with the center letter
    for word in word_list[:]:
        if must_letter not in word:
            word_list.remove(word)
        elif len(word)<4:
            word_list.remove(word)
    
    #sift through words to see if they contain letters not in the list
    other_letters += must_letter
    for word in word_list[:]:
        for letter in word:
            if letter not in other_letters:
                word_list.remove(word)
                break
    
    #sort them by length
    words = sorted(word_list, key=len)
    return words
        

def play_game(must_letter, other_letters):
     #input unknown letters of word as ? to tell program you don't know

    #get initial word list
    words = get_dictionary_word_list()

    #get the updated list of words
    words2 = words_could_be(words, must_letter, other_letters)

    #print what words it could be
    print(words2)
'''
if __name__ == '__main__':
    # Map command line arguments to function arguments.
    play_game(*sys.argv[1:])
'''
play_game('t','inxmec')