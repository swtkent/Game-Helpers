# prime_mutiprocessing.py

import time
import math
from multiprocessing import Pool, freeze_support
from itertools import combinations, permutations
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict


#constants
NUMBERS = [str(num) for num in range(10)]
OPERATORS = ['*','+','-','/']
'''
*	42	asterisk
+	43	plus sign
,	44	comma
-	45	hyphen
.	46	period
/	47	slash
0	48	digit 0
1	49	digit 1
2	50	digit 2
3	51	digit 3
4	52	digit 4
5	53	digit 5
6	54	digit 6
7	55	digit 7
8	56	digit 8
9	57	digit 9
:	58	colon
;	59	semicolon
<	60	less-than
=	61	equals-to
'''
OPERATOR_ASCII= [42,43,45,47]


#tell if left hand side is syntaxically correct
def lefthand_is_possible(combo):
    #see if starts with zero
    if combo[0]=='0' or combo[0] in OPERATORS:
        return False

    #check if starts/ends with operator
    if combo[0] in OPERATORS or combo[-1] in OPERATORS:
        return False
    
    #check if there are two operators next to each other
    for combo_spot in range(len(combo)-1):
        if combo[combo_spot] in OPERATORS and combo[combo_spot+1] in OPERATORS:
            return False
    
    #check if there are no operators
    num_ops = 0
    for character in combo:       
        num_ops+=1  if character in OPERATORS else num_ops
    if num_ops==0:
        return False

    #check if there are any zeros by themselves or lead the section in between operators
    #have to individual string split because of asterisk symbol
    for op in OPERATORS:
        res = str.split(combo,op)
        for number in res:
            if number[0]=='0':
                return False
    
    #it's good otherwise
    return combo


#evaluate equation
def eval_eqn(eqn):
    if eval(eqn) < 0 or eval(eqn)%1!=0:
        return None
    full_eqn = eqn + '=' + str(int(eval(eqn)))
    return full_eqn


#turn set into a string to add to list
def turn_into_equation(combo):
    return_string = ''
    for character in combo:
        return_string+=character
    return return_string


#create list of all potential equations for Nerdle
#remember to readd 0 as a possibility for the case of =0
def get_nerdle_equation_list(equation_length=8, equal_spots=[5,6,7]):
    num_op_combo = NUMBERS + OPERATORS

    #create the possible combinations for left and right handed sides
    valid_equations = []
    ttl_combos = 0
    for spot_diff in equal_spots:

        #create list of possible characters for left and right handed sides
        full_num_op_combo = ''
        full_num_combo = []
        for num_op in num_op_combo:
            lefthand_append_list = num_op*(spot_diff-1)
            full_num_op_combo+=lefthand_append_list


        #create the combinations
        lefthand_combinations_list = []        
        pool = Pool(processes=12)
        final_list = [[]]
        a_string = ''.join(num_op_combo)
        groups = [num_op_combo] * (spot_diff-1)
        for i in groups:
            final_list = [x+[y] for x in final_list for y in i]
        lefthand_combinations_list = [''.join(item) for item in final_list]
        #print(lefthand_combinations_list)
        #impmort pdb;pdb.set_trace()
        
        #limit combinations to be3 syntaxically accurate
        lefthand_combo_list = []        
        pool = Pool(processes=12)
        for left_result in tqdm(pool.map(lefthand_is_possible, lefthand_combinations_list), total=len(lefthand_combinations_list)):
#         for i in tqdm(range(len(lefthand_combinations_list))):
#            left_result = lefthand_is_possible(lefthand_combinations_list[i])
            if left_result!=False:
                lefthand_combo_list.append(left_result)
        #impmort pdb;pdb.set_trace()

        #run through the syntaxically correct line to see if can add it to list of equations
        spot_valid_equations = []
        for answer in tqdm(pool.map(eval_eqn, lefthand_combo_list), total=len(lefthand_combo_list)):
            if answer!=None:
                if len(answer)==equation_length:
                    spot_valid_equations.append(answer)
        #impmort pdb;pdb.set_trace()

        print(f'{spot_diff}:\t\t{len(lefthand_combinations_list)}\t->\t{len(lefthand_combo_list)}\t->\t{len(spot_valid_equations)}')
        valid_equations.extend(spot_valid_equations)
    return valid_equations


#occurrency and spot
def char_spot_occurrency(equation_list, equation_length):
    
    #get the list of operators and dictionary for summing up
    operators = OPERATORS# + ['=']
    operator_dict = {}
    for op in operators:
        operator_dict[op] = np.zeros(shape=(1,equation_length))


    number_arr = np.zeros(shape=(10,equation_length))
    operator_arr = np.zeros(shape=(len(operators),equation_length))
    equal_list = [0 for x in range(equation_length)]
    for eqn in equation_list:
        for i in range(len(eqn)):
            character = eqn[i]
            if character in NUMBERS:
                num_ascii = ord(character) - 48
                number_arr[num_ascii][i] += 1
            elif character in OPERATORS:
                operator_dict[character][0][i] += 1
            elif character=='=':
                equal_list[i] += 1
    
    #convert operator dictionary into an array
    for i in range(len(operators)):
        operator_arr[i] = operator_dict[operators[i]]

    return number_arr, operator_arr, equal_list


#create dictionary of how often equations' characters appear
def char_occurrency(characters, char_val_list):

    char_dict = {}
    for char, char_val in zip(characters, char_val_list):
        char_dict[char] = char_val
    return OrderedDict(sorted(char_dict.items()))


#print what equation has the highest char spot occurrency and another that has the highest char occurrency
def highest_equation_score(equation_list, equation_length=8):
    #pdb.set_trace()

    #get the intensities
    number_arr, operator_arr, equal_list = char_spot_occurrency(equation_list, equation_length)

    #reduce the equation list down to only those with all different characters
    for eqn in equation_list[:]:
        eqn_as_set = set(eqn)
        if len(eqn_as_set)<equation_length:
            equation_list.remove(eqn)

    #score each equation based on the character scores
    max_equation_score = 0
    max_equations = []
    for i in range(len(equation_list)):
        equation = equation_list[i]
        equation_score = 0
        for char_spot in range(len(equation)):
            char = equation[char_spot]
            if char in NUMBERS:
                char_score = number_arr[ord(char)-48][char_spot]
            elif char in OPERATORS:
                char_row = OPERATORS.index(char)
                char_score = operator_arr[char_row][char_spot]
            elif char=='=':
                char_score = equal_list[char_spot]
            equation_score += char_score
        if equation_score > max_equation_score:
            max_equation_score = equation_score
            max_equations = []
            max_equations.append(equation)
        elif equation_score == max_equation_score:
            max_equations.append(equation)
    if len(max_equations)==1:
        print('Equation with Highest Character Spot Frequency: ' + max_equations[0])
    else:
        print('Equations with Highest Character Spot Frequency: ' + str(max_equations))

    #convert the information to dictionaries for the bar graphs
    number_list = np.ndarray.sum(number_arr, axis=1)
    operator_list = np.ndarray.sum(operator_arr, axis=1)
    number_dict = char_occurrency(NUMBERS,number_list)
    operator_dict = char_occurrency(OPERATORS,operator_list)

    #score each equation based on frequency of characters regardless of location
    max_equation_score = 0
    max_equations = []
    for i in range(len(equation_list)):
        equation = equation_list[i]
        equation_score = 0
        for char in equation:
            if char in NUMBERS:
                equation_score += number_dict[char]
            elif char in OPERATORS:
                equation_score += operator_dict[char]
            elif char=='=':
                equation_score += equal_list[equation.index(char)]                
        if equation_score > max_equation_score:
            max_equation_score = equation_score
            max_equations = []
            max_equations.append(equation)
        elif equation_score == max_equation_score:
            max_equations.append(equation)
    if len(max_equations)==1:
        print('Equation with Highest Character Frequency: ' + max_equations[0])
    else:
        print('Equations with Highest Character Frequency: ' + str(max_equations))


def character_spot_occurrency_graph(equation_list, equation_length=8):

    #get the intensities
    number_arr, operator_arr, equal_list = char_spot_occurrency(equation_list, equation_length)

    #convert the information to dictionaries for the bar graphs
    number_list = np.ndarray.sum(number_arr, axis=1)
    operator_list = np.ndarray.sum(operator_arr, axis=1)
    number_dict = char_occurrency(NUMBERS,number_list)
    operator_dict = char_occurrency(OPERATORS,operator_list)
    equal_dict = char_occurrency(NUMBERS,equal_list)

    #plot the equals list
    plt.figure()
    plt.bar(equal_dict.keys(), equal_dict.values())
    plt.xlabel('Locations to Find the Equals Sign')
    plt.ylabel('Frequency of Equals Sign')
    plt.title('Frequency of Equals Sign in Each Location')

    #plot the bar graphs
    plt.figure()
    plt.subplot(2,2,1)
    plt.bar(number_dict.keys(), number_dict.values())
    plt.xlabel('Numbers in Equation')
    plt.ylabel('Frequency of Numbers')
    plt.title('Frequency of Numbers in Valid Equations')
    plt.subplot(2,2,2)
    plt.bar(operator_dict.keys(), operator_dict.values())
    plt.xlabel('Operators in Equation')
    plt.ylabel('Frequency of Operators')
    plt.title('Frequency of Operators in Valid Equations')



    #plot the number pmeshcolor
    character_nums = [x for x in range(10)]
    characters = [chr(x+48) for x in character_nums]
    character_spots = [x for x in range(equation_length)]
    x, y = np.meshgrid(character_nums, character_spots)
    plt.subplot(2,2,3)
    plt.pcolormesh(x, y, number_arr.transpose(), cmap='cool')
    plt.colorbar() #need a colorbar to show the intensity scale
    plt.xticks(character_nums, characters)
    plt.yticks(character_spots, [x+1 for x in character_spots])
    plt.title('Occurrency of Numbers and Where')

    #now again but the operators
    operator_ascii2 = [x for x in range(len(OPERATOR_ASCII))]
    operator_characters = [chr(x) for x in OPERATOR_ASCII]
    x,y = np.meshgrid(operator_ascii2, character_spots)
    plt.subplot(2,2,4)
    plt.pcolormesh(x,y, operator_arr.transpose(), cmap='cool')
    plt.colorbar() #need a colorbar to show the intensity scale
    plt.xticks(operator_ascii2, operator_characters)
    plt.yticks(character_spots, [x+1 for x in character_spots])
    plt.title('Occurrency of Operators and Where')
    plt.show()

    #give an update on best equation(s) to use
    highest_equation_score(equation_list, equation_length)


#find the locations that each 
def find_equation_occurrency(equation_length=8, equal_spots=[5,6,7]):

    #get the list of equations first
    valid_equations = get_nerdle_equation_list(equation_length=equation_length, equal_spots=equal_spots)

    #split the equation strings into an array that sums up the number of times each character appears
    character_spot_occurrency_graph(equation_list=valid_equations, equation_length=equation_length)
    
    return valid_equations


#update word list to be just the words it could be given a first try
def equations_could_be(eqn_list, known_locations, known_characters, characters_cant_be):
    #input unknown letters of word as ? to tell program you don't know

    #sift through the letters known and eliminate
    ##pdb.set_trace()
    eqn_list2 = eqn_list[:]
    for character_pos in range(len(known_locations)):
        character = known_locations[character_pos]
        if character!='?':
            for eqn in eqn_list2[:]:
                if character not in eqn:
                    eqn_list2.remove(eqn)
                elif eqn[character_pos] is not character:
                    eqn_list2.remove(eqn)
    #sift through letters known but don't know location
    for character in known_characters.keys():
        for eqn in eqn_list2[:]:
            if character not in eqn:
                eqn_list2.remove(eqn)
            else:
                for spot in known_characters[character]:
                    if eqn[spot-1] is character:
                        eqn_list2.remove(eqn)
                        break
    #sift through the letters not in there
    for character in characters_cant_be:
        for eqn in eqn_list2[:]:
            if character in eqn:
                eqn_list2.remove(eqn)
    return eqn_list2



def game_helper(known_locations, known_characters, characters_cant_be, equal_spots = [5,6,7]):
     #input unknown letters of word as ? to tell program you don't know

    #get initial equation list
    equation_length = len(known_locations)
    eqn_list = get_nerdle_equation_list(equation_length=equation_length, equal_spots=equal_spots)

    #get the updated list of words
    eqns2 = equations_could_be(eqn_list, known_locations, known_characters, characters_cant_be)

    #update best equation(s)
    print(f'{len(eqn_list)} real equations\t->\t{len(eqns2)} potential equations')
    highest_equation_score(eqns2, equation_length)

    #show the layout of the new letters and locations likely and best equation
    #split the equation strings into an array that sums up the number of times each character appears
    character_spot_occurrency_graph(equation_list=eqn_list, equation_length=equation_length)
    
    plt.show()


if __name__ == "__main__":
    freeze_support()   # required to use multiprocessing
    #valid_equations = get_nerdle_equation_list()
    #highest_equation_score(valid_equations)
    game_helper(known_locations='???/?=7?', known_characters={}, characters_cant_be='-+03465', equal_spots=[6])

