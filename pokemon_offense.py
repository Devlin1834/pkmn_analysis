# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 06:46:36 2019

@author: Devlin
"""
###############################################################################
## The Inputs #################################################################
# Offense #####################################################################
# Three lists in a list: 1st - 2x, 2nd - .5x, 3rd - 0x ########################
# The numbers correspond to types: 1 + the key of the dictionary ##############
# This is offensive based, so we read this data as Normal deals .5x to 6 and 
# 0x to 8 #####################################################################
###############################################################################

normal = [[], [6], [8]]
fighting = [[1, 6, 9, 15, 17], [3, 4, 7, 14, 18], [8]]
flying = [[7, 12, 2], [6, 9, 13], []]
poison = [[12, 18], [4, 5, 6, 8], [9]]
ground = [[4, 6, 9, 10, 13], [7, 12], [3]]
rock = [[3, 7, 10, 15], [2, 5, 9], []]
bug = [[12, 14, 17], [2, 3, 4, 8, 9, 10], []]
ghost = [[8, 14], [17], [1]]
steel = [[6, 15, 18], [9, 10, 11, 13], []]
fire = [[7, 9, 12, 15], [6, 10, 11, 16], []]
water = [[5, 6, 10], [11, 12, 16], []]
grass = [[5, 6, 11], [3, 4, 7, 9, 10, 12, 16], []]
electric = [[3, 11], [12, 13, 16], [5]]
psychic = [[2, 4], [9, 14], [17]]
ice = [[3, 5, 12, 16], [9, 10, 11, 15], []]
dragon = [[16], [6], [18]]
dark = [[8, 14], [2, 17, 18], []]
fairy = [[2, 16, 17], [4, 9, 10], []]

# t is a list of types, for future use
t = ["normal", "fighting", "flying", "poison", "ground", "rock", "bug", "ghost", "steel", "fire", "water", "grass", "electric", "psychic", "ice", "dragon", "dark", "fairy"]
# a list of all the lists above
offense_list = [normal, fighting, flying, poison, ground, rock, bug, ghost, steel, fire, water, grass, electric, psychic, ice, dragon, dark, fairy]

offense_dict = {0:[],  #Normal
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
## Building the Dictionary ####################################################
## The whole point of these first three sections is because I didn't feel like 
## writing out the whole type efectiveness table, though that might have been
## more parimonious ###########################################################
## For a subject type's list of lists in offense list: it appends a mini list,
## [type from t, efectiveness], to the subject type's dictionary list #########
## ns is for finding ts, listing every type in the dictionary list ############
## ts is all types recieving 1x damage, for appending to the dictionary list ##
###############################################################################
## For clarity: here, when we say Fighing deals 2x to Normal, Fighting is the 
## subject type and Normal is the affecting type ############################## 
###############################################################################

# 0 - Supereffective, deals 2x
# 1 - Not Very Effective, deals .5x
# 2 - Has No Effect, deals 0x
for subject_type in offense_list:
    for i in subject_type[0]:
        offense_dict[offense_list.index(subject_type)].append([t[i-1], 2])
    for i in subject_type[1]:
        offense_dict[offense_list.index(subject_type)].append([t[i-1], .5])
    for i in subject_type[2]:
        offense_dict[offense_list.index(subject_type)].append([t[i-1], 0])
    ns = [i[0] for i in offense_dict[offense_list.index(subject_type)]]
    ts = [i for i in t if i not in ns]
    for i in ts:
        offense_dict[offense_list.index(subject_type)].append([i, 1])

###############################################################################
## The ALMIGHTY CALCULATOR ####################################################
## For finding the full scope of coverage for a dual STAB #####################
###############################################################################
## So it takes two types as inputs, the second is set to False by default #####
## If the second is the same as the first or is False, its an easy answer #####
## When there's two types, it loads the dictionary list for each. Then it loops
## through matching types and taking the max effectiveness between the two. 
## Then it creates a new list like the dictionary lists, [type, effectiveness]
## It returns this new list with the types sorted aplhabetically ##############
###############################################################################
        
def offense_calculator(first, second = False):        
    
    if second == False or second == first:
        return offense_dict[t.index(first.lower())]
    
    a = offense_dict[t.index(first.lower())]
    b = offense_dict[t.index(second.lower())]
    n = []
    
    for i in a:
        for e in b:
            if i[0] == e[0]:
                n.append([i[0], max(i[1], e[1])])
        
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

    stab_coverage = []
    stab_holes = []
    for i in offense_calculator(first_type, second_type):
        print(i[0] + ": " + str(i[1]))
        
        if i[1] == 2:
            stab_coverage.append(i[0])
        elif i[1] == .5 or i[1] == 0:
            stab_holes.append(i[0])
        
    print("STAB Coverage: {} types".format(len(stab_coverage)))
    print("STAB Holes: {} types".format(len(stab_holes)))
    if len(stab_holes) != 0:
        effective_coverage = (len(stab_coverage)/len(stab_holes))
    else:
        effective_coverage = "PERFECT"
    print("Effective Coverage: {}".format(effective_coverage))
          
###############################################################################
## Setup for Further Analysis                                               ###
## Determining the most effective Offensive Type                            ###
###############################################################################

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
#        for e in offense_calculator(i, s):
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
#[['normal', 369.5],   #
# ['dragon', 385.5],   #
# ['poison', 390.5],   #
# ['electric', 398.5], #         1) Ice/Fighting and Ice/Ground are tied for top
# ['psychic', 398.5],  #         1) Normal/Dragon is the worst offensive typing
# ['grass', 401.5],    #
# ['dark', 401.5],     #
# ['bug', 402.5],      #
# ['ghost', 403.5],    #
# ['steel', 407.0],    #
# ['flying', 409.5],   #
# ['fairy', 410.0],    #
# ['water', 412.0],    #
# ['fire', 422.5],     #
# ['ice', 423.0],      #
# ['rock', 426.5],     #
# ['fighting', 437.5], # 
# ['ground', 445.0]]   #
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
#plt.title("Offenseive capabilities of Pokemon Types")
#plt.xlabel("Types")
#plt.ylabel("Offensive Skill (Higher is better)")
#plt.show()
#
#theta = np.std(counts)
#xbar = np.mean(counts)
#
#z_ground = (445 - xbar)/theta
#z_normal = (369.5 - xbar)/theta
#
#print("Ground is statistically significatly better offensively: z of " + str(round(z_ground, 2)))
#print("Normal is statistically significatly worse offensvely: z of " + str(round(z_normal, 2)))
#    