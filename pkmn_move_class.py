# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 07:04:53 2019

@author: Devlin
"""

import csv
import numpy as np
import pokemon
import table_gen2

class Move():
    def __init__(self, name, gen, move_type_id, power, pp, accuracy, priority, damage_class_id, is_z, signature):
        self.name = name                          
        self.gen = gen                            
        self.move_type_id = int(move_type_id)     
        self.priotity = int(priority)             
        self.pp = int(pp)
                         
       ############################################        
        if power == '':                           #          #   # 
            self.power = 0                        #          #   #
        else:                                     #          #   #
            self.power = int(power)               #           ###
       ############################################
        if accuracy == '':                        #           ###     
            self.accuracy = 1                     #          #    
        else:                                     #          #  # 
            self.accuracy = int(accuracy)/100     #           ###
       ############################################            
        if is_z == '':                            #          #
            self.is_z = False                     #          # 
        else:                                     #          #
            self.is_z = True                      #          ##### 
       ############################################        
        if signature == '':                       #          #   #
            self.signature = False                #           # #
        else:                                     #            #
            self.signature = True                 #            #
       ############################################   
            
        self.move_type = pokemon.t[self.move_type_id - 1]

        damage_class_name = ['', 'Status', 'Physical', 'Special']
        self.damage_class = damage_class_name[int(damage_class_id)]   
            
        self.expected_damage = self.power * self.accuracy
    
    def __repr__(self):
        return self.name, self.move_type
        
    def __str__(self):
        if self.is_z == True:
            return '{}: {} {} Z-move dealing {} expected damage'.format(self.name, self.damage_class, self.move_type.capitalize(), self.expected_damage)
        else:
            return '{}: {} {} move dealing {} expected damage'.format(self.name, self.damage_class, self.move_type.capitalize(), self.expected_damage)

###############################################################################
## DATA ANALYSIS #############  ^  ^  ^  ^  ^   ################## FUN STUFF ##
##   |   |   |   #############  |  |  |  |  |   ##################  |  |  |  ##
##   V   V   V   ############# CLASS DEFINITION ##################  V  V  V  ##
###############################################################################
            
moves_refference = list(csv.reader(open("C:\\Users\\Devlin\\Documents\\moves.csv")))
moves_reduced = [move[1:11] for move in moves_refference]
for move in moves_reduced:
    mname = move[0].replace('-', ' ')
    capped_name = [word.capitalize() for word in mname.split()]
    move[0] = ' '.join(capped_name)
all_moves = [Move(*i) for i in moves_reduced]

###############################################################################
# Excluding Z moves and Signature moves ####### Because they're outliers, duh #
# ALL MOVES ###################################################################

move_expected_damage = [move.expected_damage for move in all_moves if move.damage_class != 'Status' and move.is_z == False and move.signature == False]
move_mean = np.mean(move_expected_damage)

moves_by_type = {0:[],            #Normal
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

for move in [x for x in all_moves if x.damage_class != 'Status' and x.is_z == False and x.signature == False]:
    moves_by_type[move.move_type_id - 1].append(move)

move_means_by_type = ['' for i in range(18)]
for key in moves_by_type:
    expected_damages = [move.expected_damage for move in moves_by_type[key]]
    move_means_by_type[key] = round(np.mean(expected_damages), 2)

###############################################################################
# PHYSICAL MOVES ##############################################################
    
physical_moves = [move for move in all_moves if move.damage_class == 'Physical' and move.is_z == False and move.signature == False]
pmove_expected_damage = [move.expected_damage for move in physical_moves]
pmove_mean = np.mean(pmove_expected_damage)
pmoves_by_type = {0:[],           #Normal
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

for move in physical_moves:
    pmoves_by_type[move.move_type_id - 1].append(move)

pmove_means_by_type = ['' for i in range(18)]
for key in pmoves_by_type:
    expected_damages = [move.expected_damage for move in pmoves_by_type[key]]
    pmove_means_by_type[key] = round(np.mean(expected_damages), 2)

###############################################################################
# SPECIAL MOVES ###############################################################
    
special_moves = [move for move in all_moves if move.damage_class == 'Special' and move.is_z == False and move.signature == False]
smove_expected_damage = [move.expected_damage for move in special_moves]
smove_mean = np.mean(smove_expected_damage)
smoves_by_type = {0:[],           #Normal
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

for move in special_moves:
    smoves_by_type[move.move_type_id - 1].append(move)

smove_means_by_type = ['' for i in range(18)]
for key in smoves_by_type:
    expected_damages = [move.expected_damage for move in smoves_by_type[key]]
    smove_means_by_type[key] = round(np.mean(expected_damages), 2)

###############################################################################
# TABLE GENERATION ############################################################
    
moves_consolodated = [str(i) for i in move_means_by_type]
pmoves_consolodated = [str(i) for i in pmove_means_by_type]
smoves_consolodated = [str(i) for i in smove_means_by_type]
damage_classes = ['All', 'Physical', 'Special']
all_rows = [i.upper() for i in pokemon.t]
summary = [str(round(move_mean, 2)), str(round(pmove_mean, 2)), str(round(smove_mean, 2))]
move_data = [moves_consolodated, pmoves_consolodated, smoves_consolodated]

if __name__ == "__main__":
    table_gen2.table_gen(row_names = all_rows, col_names = damage_classes, list_of_lists = move_data, summary_row = summary)
    ## Mean Expected Damage is distributed uniformly accross type so its not a significant factor in type selection
