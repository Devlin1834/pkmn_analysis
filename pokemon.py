# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 06:46:36 2019

@author: Devlin
"""
###############################################################################
## The Inputs #################################################################
# Deffense ####################################################################
# Three lists in a list: 1st - 2x, 2nd - .5x, 3rd - 0x ########################
# The numbers correspond to types: 1 + the key of the dictionary ##############
# This is defensive based, so we read this data as Normal takes 2x from 2 and
# 0x from 8 ###################################################################
###############################################################################

normal = [[2], [], [8]]
fighting = [[3, 14, 18], [6, 7, 17], []]
flying = [[6, 13, 15], [2, 7, 12], [5]]
poison = [[5, 14], [2, 4, 7, 12, 18], []]
ground = [[11, 12, 15], [4, 6], [13]]
rock = [[2, 5, 9, 11, 12], [1, 3, 4, 10], []]
bug = [[3, 6, 10], [2, 5, 12], []]
ghost = [[8, 17], [4, 7], [1, 2]]
steel = [[2, 5, 10], [1, 3, 6, 7, 9, 12, 14, 15, 16, 18], [4]]
fire = [[5, 6, 11], [7, 9, 10, 12, 15, 18], []]
water = [[12, 13], [9, 10, 11, 15], []]
grass = [[3, 4, 7, 10, 15], [5, 11, 12, 13], []]
electric = [[5], [3, 9, 13], []]
psychic = [[7, 8, 17], [2, 14], []]
ice = [[2, 6, 9, 10], [15], []]
dragon = [[16, 15, 18], [10, 11, 12, 13], []]
dark = [[2, 7, 18], [8, 17], [14]]
fairy = [[4, 9], [2, 17], [16]]

# t is a list of types, for future use
t = ["normal", "fighting", "flying", "poison", "ground", "rock", "bug", "ghost", "steel", "fire", "water", "grass", "electric", "psychic", "ice", "dragon", "dark", "fairy"]
# a list of all the lists above
deffense_list = [normal, fighting, flying, poison, ground, rock, bug, ghost, steel, fire, water, grass, electric, psychic, ice, dragon, dark, fairy]

deffense_dict = {0:[], #Normal
       1:[],           #Fighting
       2:[],           #Flying
       3:[],           #Poison
       4:[],           #Ground
       5:[],           #Rock
       6:[],           #Bug
       7:[],           #Ghost
       8:[],           #Steel
       9:[],           #Fire
       10:[],          #Water
       11:[],          #Grass
       12:[],          #Electric
       13:[],          #Psychic
       14:[],          #Ice
       15:[],          #Dragon
       16:[],          #Dark
       17:[]           #Fairy
       }

###############################################################################
## Bulding the Dictionary #####################################################
## The whole point of these first three sections is because I didn't feel like 
## writing out the whole type efectiveness table, though that might have been
## more parimonious ###########################################################
## For a subject-type's list of lists in deffense list: it appends a mini list,
## [type from t, efectiveness], to the subject-type's dictionary list #########
## ns is for finding ts, listing every type in the dictionary list ############
## ts is every type dealing 1x damage, to be appended to the dictionary list ##
###############################################################################
## For clarity: here, when we say Normal takes 2x from Fighting, Normal is the 
## subject-type and Fighting is the affecting-type ############################ 
###############################################################################

# 0 - Weak, takes 2x
# 1 - Resists, takes .5x
# 2 - Immune, takes 0x
for subject_type in deffense_list:
    for i in subject_type[0]:
        deffense_dict[deffense_list.index(subject_type)].append([t[i-1], 2])
    for i in subject_type[1]:
        deffense_dict[deffense_list.index(subject_type)].append([t[i-1], .5])
    for i in subject_type[2]:
        deffense_dict[deffense_list.index(subject_type)].append([t[i-1], 0])
    ns = [i[0] for i in deffense_dict[deffense_list.index(subject_type)]]
    ts = [i for i in t if i not in ns]
    for i in ts:
        deffense_dict[deffense_list.index(subject_type)].append([i, 1])

###############################################################################
## The ALMIGHTY CALCULATOR ####################################################
## For finding weaknesses and resistences for dual typings ####################
###############################################################################
## So it takes two types as inputs, the second is set to False by default #####
## If the second is the same as the first or is False, its an easy answer #####
## When there's two types, it loads the dictionary list for each. Then it loops
## through matching types and mutiplying their effectiveness together. Then it
## creates a new list like a dictionary list, [[type, effectiveness],...]. 
## It returns this new list with the types sorted aplhabetically ##############
###############################################################################
        
def deffense_calculator(first, second = False):        
    
    if second == False or second == first:
        return deffense_dict[t.index(first.lower())]
    
    a = deffense_dict[t.index(first.lower())]
    b = deffense_dict[t.index(second.lower())]
    n = []
    
    for i in a:
        for e in b:
            if i[0] == e[0]:
                n.append([i[0], i[1] * e[1]])
        
    return sorted(n, key = lambda x: x[0])

###############################################################################
## Setup for using the function                                             ###
## Running from powershell                                                  ###
###############################################################################
    
if __name__ == "__main__":
    while True:
        first_type = input("Type 1 >> ").lower()
        if first_type not in t:
            print("Not a Valid Type")
        else:
            break
    
    while True:
        second_type = input("Type 2 >> ").lower()
        if second_type not in t:
            second_type = False
        break
        
    for i in deffense_calculator(first_type, second_type):
        print(i[0] + ": " + str(i[1]))
    
###############################################################################
## Setup for Further Analysis                                               ###
## Determining the most effective Defensve Type                             ###
###############################################################################
#
#dos = {0:[],
#       1:[],
#       2:[],
#       3:[],
#       4:[],
#       5:[],
#       6:[],
#       7:[],
#       8:[],
#       9:[],
#       10:[],
#       11:[],
#       12:[],
#       13:[],
#       14:[],
#       15:[],
#       16:[],
#       17:[]
#       }
#
#for i in t:
#    for s in t:
#        skill = []
#        for e in deffense_calculator(i, s):
#            skill.append(e[1])
#        dos[t.index(i)].append([s, sum(skill)])
#        
#final = []
#for key in dos:
#    add = [i[1] for i in dos[key]]
#    final.append([t[key], sum(add)])
#    
#final_sorted = sorted(final, key = lambda x: x[1])

## Results #############
#[['steel', 293.5],    #          Suprise Revelations:
# ['ghost', 317.75],   #       1) Psychic is a worse defensive type than bug
# ['poison', 327.75],  #       2) Dark is a worse defensie type than fairy
# ['electric', 329.25],#       3) Water made the top 5, Grass made the bottom 3
# ['water', 330.25],   #       4) Steel/Flying is the best defensive dual typing
# ['fairy', 333.5],    #       5) Ice/Rock is the wost defensive dual typing
# ['normal', 336.5],   #
# ['fire', 336.75],    #
# ['flying', 341.5],   #
# ['dragon', 352.25],  #
# ['ground', 352.75],  #
# ['dark', 353.0],     #
# ['fighting', 360.5], #
# ['bug', 363.25],     #
# ['psychic', 368.75], #
# ['grass', 385.75],   #
# ['rock', 388.75],    #
# ['ice', 398.75]]     #
########################

###############################################################################
## Making a Graph #############################################################
###############################################################################
#import matplotlib.pyplot as plt
#import numpy as np
#
#xs = [i[0] for i in final_sorted]
#counts = [i[1] for i in final_sorted]
#x_enum = [e for e, i in enumerate(xs)]
#
#plt.figure(figsize = (13,5))
#plt.bar(x_enum, counts)
#plt.xticks(x_enum, xs)
#plt.title("Defensive capabilities of Pokemon Types")
#plt.xlabel("Types")
#plt.ylabel("Defensive Skill (lower is better)")
#plt.show()
#
#theta = np.std(counts)
#xbar = np.mean(counts)
#
#z_analysisteel = (293.5 - xbar)/theta
#z_ice = (398.75 - xbar)/theta
#
#print("Steel is statistically significatly better deffensively: z of " + str(round(z_analysisteel, 2)))
#print("Ice is statistically significatly worse deffensively: z of " + str(round(z_ice, 2)))
    