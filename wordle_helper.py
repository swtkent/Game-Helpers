from english_words import english_words_lower_alpha_set
import matplotlib.pyplot as plt
from collections import OrderedDict
import numpy as np
from tqdm import tqdm

#list of words known not to work in Wordle/Quordle
WORDS_CANT_BE = ['delhi']
WORDS_CAN_BE = ['soare', 'smore', 'ninja']


#get all of the words in the english dictionary
def get_dictionary_word_list(remove_words=True):
    word_list = list(english_words_lower_alpha_set)
    
    #remove random nonalpha symbols known to be in word list
    for word in word_list[:]:
        if '.' in word or '&' in word:
            word_list.remove(word)

    #remove words known not to work for wordle/quordle
    if remove_words is True:
        for word in WORDS_CANT_BE:
            word_list.remove(word)

    #add words known not in this dictionary but are in wordle/quordle
    word_list.extend(WORDS_CAN_BE)

    return sorted(word_list)
    

#get all words of certain length
def get_words_of_size(word_list, word_length=5): #built for wordle
    new_word_list = []
    for word in word_list:
        if len(word)==word_length:
            new_word_list.append(word)
    return new_word_list


#break into vowels and consonants
def break_letter_type(letter_dict):
    vowels = ['a','e','i','o','u','y']
    vowel_dict = {}
    consonant_dict = {}
    for letter in letter_dict:
        if letter in vowels:
            vowel_dict[letter] = letter_dict[letter]
        else:
            consonant_dict[letter] = letter_dict[letter]
    return vowel_dict, consonant_dict


#create dictionary of how often words' letters appear
def letter_occurrency(word_list):
    letter_dict = {}
    for word in word_list:
        for letter in word:
            if letter in letter_dict:
                letter_dict[letter] += 1
            else:
                letter_dict[letter] = 1
    return OrderedDict(sorted(letter_dict.items()))


def letter_spot_occurrency(word_list, word_length):
    
    letter_arr = np.zeros(shape=(26,word_length))
    for word in word_list:
        for i in range(len(word)):
            letter = word[i]
            let_num = ord(letter) - 97
            letter_arr[let_num][i] += 1
    return letter_arr

#print what word has the highest letter spot occurrency and another that has the highest letter occurrency
def highest_word_score(word_list, word_length):
    #pdb.set_trace()

    #just in case
    word_list = get_words_of_size(word_list, word_length)

    #get the array of letter scores
    letter_arr = letter_spot_occurrency(word_list, word_length)

    #score each word based on the letter scores
    max_word_score = 0
    max_word = 'ERROR'
    for i in range(len(word_list)):
        word = word_list[i]
        word_score = 0
        for letter_spot in range(len(word)):
            letter = word[letter_spot]
            letter_score = letter_arr[ord(letter)-97][letter_spot]
            word_score += letter_score
        if word_score > max_word_score:
            max_word_score = word_score
            max_word = word
    print('Word with Highest Letter Spot Frequency: ' + max_word)

    #score each word based on frequency of letters regardless of location
    letter_frequency = letter_occurrency(word_list)
    max_word_score = 0
    for i in range(len(word_list)):
        word = word_list[i]
        for letter in word:
            ##pdb.set_trace()
            word_score += letter_frequency[letter]
        if word_score> max_word_score:
            max_word_score = word_score
            max_word = word
    print('Word with Highest Letter Score: ' + max_word)


def letter_spot_occurrency_graph(word_list, word_length=5):
    
    print(word_list)
    #pdb.set_trace()
        #update the word set just in case
    ws2 = get_words_of_size(word_list, word_length)

    #get the intensities
    letter_arr = letter_spot_occurrency(ws2, word_length)

    #return the word with the highest score
    highest_word_score(ws2, word_length)

    #setup the 2D grid with Numpy
    letter_nums = [x for x in range(26)]
    letters = [chr(x+97) for x in letter_nums]
    letter_spots = [x for x in range(word_length)]
    x, y = np.meshgrid(letter_nums, letter_spots)

    #now just plug the data into pcolormesh, it's that easy!
    plt.subplot(1,2,1)
    plt.pcolormesh(x, y, letter_arr.transpose(), cmap='cool')
    plt.colorbar() #need a colorbar to show the intensity scale
    plt.xticks(letter_nums, letters)
    plt.yticks(letter_spots, [x+1 for x in letter_spots])
    plt.title('Occurrency of Letters and Where')

    #now again but split into vowels and consonants
    vowel_nums = [0,4,8,14,20,24]
    vowel_nums2 = [x for x in range(len(vowel_nums))]
    vowel_arr = letter_arr[[x for x in vowel_nums],:]
    vowel_letters = [chr(x+97) for x in vowel_nums]
    x,y = np.meshgrid(vowel_nums2, letter_spots)
    plt.subplot(2,2,2)
    plt.pcolormesh(x,y, vowel_arr.transpose(), cmap='cool')
    plt.colorbar() #need a colorbar to show the intensity scale
    plt.xticks(vowel_nums2, vowel_letters)
    plt.yticks(letter_spots, [x+1 for x in letter_spots])
    plt.title('Occurrency of Vowels and Where')
    
    #now again but split into vowels and consonants
    consonant_nums = letter_nums
    for x in vowel_nums:
        consonant_nums.remove(x)
    consonant_nums2 = [x for x in range(len(consonant_nums))]
    consonant_arr = letter_arr[[x for x in consonant_nums],:]
    consonant_letters = [chr(x+97) for x in consonant_nums]
    x,y = np.meshgrid(consonant_nums2, letter_spots)
    plt.subplot(2,2,4)
    plt.pcolormesh(x,y, consonant_arr.transpose(), cmap='cool')
    plt.colorbar() #need a colorbar to show the intensity scale
    plt.xticks(consonant_nums2, consonant_letters)
    plt.yticks(letter_spots, [x+1 for x in letter_spots])
    plt.title('Occurrency of Consonants and Where')


def letter_occurrency_graph(word_list, word_length=5):

    #get the letter occurrency
    letter_dict = letter_occurrency(word_list)

    #make a bar graph out of it
    plt.figure()
    plt.subplot(1,2,1)
    plt.bar(letter_dict.keys(), letter_dict.values())
    plt.title('Frequency of Letters')

    #break them up by letter type
    vowel_dict, consonant_dict = break_letter_type(letter_dict)
    plt.subplot(2,2,2)
    plt.bar(vowel_dict.keys(), vowel_dict.values())
    plt.title('Frequency of Vowels')
    plt.subplot(2,2,4)
    plt.bar(consonant_dict.keys(), consonant_dict.values())
    plt.title('Frequency of Consonants')
        

#update word list to be just the words it could be given a first try
def words_could_be(word_list, known_locations, known_letters, letters_cant_be):
    #input unknown letters of word as ? to tell program you don't know

    #sift through the letters known and eliminate
    ##pdb.set_trace()
    for letter_pos in range(len(known_locations)):
        letter = known_locations[letter_pos]
        if letter!='?':
            for word in word_list[:]:
                if letter not in word:
                    word_list.remove(word)
                elif word[letter_pos] is not letter:
                    word_list.remove(word)
    #sift through letters known but don't know location
    for letter in known_letters.keys():
        for word in word_list[:]:
            if letter not in word:
                word_list.remove(word)
            else:
                for spot in known_letters[letter]:
                    if word[spot-1] is letter:
                        word_list.remove(word)
                        break
    #sift through the letters not in there
    for letter in letters_cant_be:
        for word in word_list[:]:
            if letter in word:
                word_list.remove(word)
    return word_list
        

#number of vowels per word
def vowels_per_word(word_length=5, include_y = True):
    vowels = ['a','e','i','o','u']
    vowels.append('y') if include_y is True else vowels
    word_list = get_dictionary_word_list()
    ws2 = get_words_of_size(word_list, word_length)
    total_vowel_counts = {}
    for word in ws2:
        vowel_count = 0
        for letter in word:
            if letter in vowels:
                vowel_count+=1
        if vowel_count in total_vowel_counts:
            total_vowel_counts[vowel_count] +=1
        else:
            total_vowel_counts[vowel_count] = 1
    plt.figure()
    plt.bar(total_vowel_counts.keys(), total_vowel_counts.values())
    plt.xlabel('Number of Vowels in Word')
    plt.ylabel('Number of Words')
    plt.title('Number of Words with Each Number of Vowels')
    plt.show()


#recursively run through word list num_words times
def word_searcher(word_list, num_words, word_length, ttl_combos = [], current_words = []):
    if current_words==[]:
        for word in tqdm(word_list):
            #check for the word adds letters already in current_words list
            words_string = word
            for word2 in current_words:
                words_string += word2
            unique_letters = set(words_string)

            #only add to current_words list if there's no overlap
            if len(unique_letters) == word_length*(len(current_words)+1):
                current_words.append(word)

                #run through again if current_words length is less than num_words needed
                if len(current_words)<num_words:
                    #don't bother with words that occur before this one in the list, they'd already be in ttl_combos
                    new_word_list = word_list[word_list.index(word)+1:]
                    ttl_combos = word_searcher(word_list=new_word_list, num_words=num_words, word_length=word_length, ttl_combos=ttl_combos, current_words=current_words)
                else:
                    ttl_combos.append(list(current_words))
                current_words.remove(word)
    else:
        for word in word_list:
            #check for the word adds letters already in current_words list
            words_string = word
            for word2 in current_words:
                words_string += word2
            unique_letters = set(words_string)

            #only add to current_words list if there's no overlap
            if len(unique_letters) == word_length*(len(current_words)+1):
                current_words.append(word)

                #run through again if current_words length is less than num_words needed
                if len(current_words)<num_words:
                    #don't bother with words that occur before this one in the list, they'd already be in ttl_combos
                    new_word_list = word_list[word_list.index(word)+1:]
                    ttl_combos = word_searcher(word_list=new_word_list, num_words=num_words, word_length=word_length, ttl_combos=ttl_combos, current_words=current_words)
                else:
                    ttl_combos.append(list(current_words))
                current_words.remove(word)
    return ttl_combos


#best words to guess to start Quordle/Wordle
def find_best_combo(word_length=5, num_words=3):

    #get the words with the length
    word_list = get_words_of_size(get_dictionary_word_list(), word_length)
    
    #find the letter occurrency
    letter_dict = letter_occurrency(word_list)
    letter_arr = letter_spot_occurrency(word_list, word_length=5)

    #get rid of words with double letters, they'll automatically be cut in the combo anyways
    for word in word_list[:]:
        yo = set(word)
        if len(yo)<word_length:
            word_list.remove(word)

    #get the list of combos possible
    ttl_combos = word_searcher(word_list=word_list, num_words=num_words, word_length=word_length)

    #run through the list and find the best word combos
    max_combo_occurrency = 0
    max_combo_spot = 0
    max_occ_words = []
    max_spot_words = []
    for word_combo in tqdm(ttl_combos):
        combo_occurrency = 0
        combo_spot = 0
        for word in word_combo:
            for letter_spot in range(len(word)):
                letter = word[letter_spot]
                combo_occurrency += letter_dict[letter]
                combo_spot += letter_arr[ord(letter)-97][letter_spot]
        max_occ_words, max_combo_occurrency = (word_combo, combo_occurrency) if combo_occurrency>max_combo_occurrency else (max_occ_words, max_combo_occurrency)
        max_spot_words, max_combo_spot = (word_combo, combo_spot) if combo_spot>max_combo_spot else (max_spot_words, max_combo_spot)

    #get the percentage chance of getting the information wanted
    max_occ_percent = max_combo_occurrency/sum(letter_dict.values())*100
    max_spot_percent = max_combo_spot/np.sum(letter_arr)*100

    #tell the user what their best choices are and what percentage of the base they make up
    print('Highest Chance of Getting Letters: ' + ', '.join(max_occ_words) + ' - ' + "{:.2f}".format(max_occ_percent) + '%')
    print('Highest Chance of Getting Letters in Their Spots: ' + ', '.join(max_spot_words) + ' - ' + "{:.2f}".format(max_spot_percent) + '%')


def game_helper(known_locations, known_letters, letters_cant_be):
     #input unknown letters of word as ? to tell program you don't know

    #get initial word list
    word_length = len(known_locations)
    words = get_words_of_size(get_dictionary_word_list(), word_length)

    #get the updated list of words
    words2 = words_could_be(words, known_locations, known_letters, letters_cant_be)

    #show the layout of the new letters and locations likely
    letter_spot_occurrency_graph(words2, word_length)
    letter_occurrency_graph(words2, word_length)
    
    plt.show()

'''
if __name__ == '__main__':
    # Map command line arguments to function arguments.
    data=json.loads(sys.argv[2])
    game_helper(sys.argv[1],data, sys.argv[3])
'''
#code used to show it works and figure out what might be a good first guess

#game_helper('?????', {},'soare')