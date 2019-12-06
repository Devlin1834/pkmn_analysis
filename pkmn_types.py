# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 06:46:36 2019

@author: Devlin
"""
###############################################################################
## The Inputs #################################################################
# Defense #####################################################################
# Three lists in a list: 1st - 2x, 2nd - .5x, 3rd - 0x ########################
# The numbers correspond to types: 1 + the key of the dictionary ##############
# This is defensive based, so we read this data as Normal takes 2x from 1 and
# 0x from 7s ###################################################################
###############################################################################
normal = [[1], [], [7]]
fighting = [[2, 13, 17], [5, 6, 16], []]
flying = [[5, 12, 14], [1, 6, 11], [4]]
poison = [[4, 13], [1, 3, 6, 11, 17], []]
ground = [[10, 11, 14], [3, 5], [12]]
rock = [[1, 4, 8, 10, 11], [0, 2, 3, 9], []]
bug = [[2, 5, 9], [1, 4, 11], []]
ghost = [[7, 16], [3, 6], [0, 1]]
steel = [[1, 4, 9], [0, 2, 5, 7, 8, 11, 13, 14, 15, 17], [3]]
fire = [[4, 5, 10], [6, 8, 9, 11, 14, 17], []]
water = [[11, 12], [8, 9, 10, 14], []]
grass = [[2, 3, 6, 9, 14], [4, 10, 11, 12], []]
electric = [[4], [2, 8, 12], []]
psychic = [[6, 7, 16], [1, 13], []]
ice = [[1, 5, 8, 9], [14], []]
dragon = [[15, 14, 17], [9, 10, 11, 12], []]
dark = [[1, 6, 17], [7, 16], [13]]
fairy = [[3, 8], [1, 16], [15]]


t = ["Normal", "Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost", "Steel", "Fire", "Water", "Grass", "Electric", "Psychic", "Ice", "Dragon", "Dark", "Fairy"]

defense_list = [normal, fighting, flying, poison, ground, rock, bug, ghost, steel, fire, water, grass, electric, psychic, ice, dragon, dark, fairy]

defense_dict = {i: [] for i in range(18)}
offense_dict = {i: [] for i in range(18)}

###############################################################################
## Bulding the Defense Dictionary #############################################
## The whole point of these first three sections is because I didn't feel like 
## writing out the whole type efectiveness table, though that might have been #
## more parimonious ###########################################################
## For a subject-type's list of lists in defense list: it appends a mini list,
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
for subject_type in defense_list:
    dex = defense_list.index(subject_type)
    subject_type_list = defense_dict[dex]
    effs = [2, .5, 0]
    for x in range(3):
        for i in subject_type[x]:
            subject_type_list.append([t[i], effs[x]])
    ns = [i[0] for i in subject_type_list]
    ts = [i for i in t if i not in ns]
    for i in ts:
        subject_type_list.append([i, 1])
        
###############################################################################
## Building the Offense Dictionary ############################################
## From here, we take the defense_dict and invert it. If Psychic takes 2x from
## Dark, then Dark must deal 2x to Phsycic. So it loops over the dictionary, ##
## then loops over the sublists in each dictionary and reassigns the values to 
## the opposite type. Essentialy we switch the Subject Types and Affecting ####
## types. I'm pretty happy with this, don't judge too harshly #################
###############################################################################     
for key in defense_dict:
    subject_list = defense_dict[key]
    subject = t[key]
    for sublist in subject_list:
        indicie = t.index(sublist[0])
        eff = sublist[1]
        offense_dict[indicie].append([subject, eff])

###############################################################################
## The DEFENSE CALCULATOR #####################################################
## For finding weaknesses and resistences for dual typings ####################
###############################################################################
## So it takes two types as inputs, the second is set to False by default #####
## If the second is the same as the first or is False, its an easy answer #####
## When there's two types, it loads the dictionary list for each. Then it loops
## through matching types and mutiplying their effectiveness together. Then it
## creates a new list like a dictionary list, [[type, effectiveness],...]. 
## It returns this new list with the types sorted aplhabetically ##############
###############################################################################        
def defense_calculator(first, second = False):        
    
    if second == False or second == first:
        return defense_dict[t.index(first)]
    else:
        a = defense_dict[t.index(first)]
        b = defense_dict[t.index(second)]
        n = []
    
        for i in a:
            for e in b:
                if i[0] == e[0]:
                    n.append([i[0], i[1] * e[1]])
        
        return sorted(n, key = lambda x: x[0])

###############################################################################
## The OFFENSE CALCULATOR #####################################################
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
        return offense_dict[t.index(first)]
    
    a = offense_dict[t.index(first)]
    b = offense_dict[t.index(second)]
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
def type_check(text):
    while True:
        ptype = input(text).capitalize()
        if ptype not in t:
            print("Not a Valid Type")
        else:
            break
        
    return ptype

###############################################################################
## To help pull instances from a list                                       ###
###############################################################################
def selectro(array, Name):
    """Yes, it's on purpose"""
    try:
        x = [i for i in array if i.name.lower() == Name][0]
    except IndexError:
        print('That name isn\'t in the list')
    else:
        return x
    
###############################################################################
## Single Energy Types ########################################################
###############################################################################
class Energy_Type():
    def __init__(self, type_id, name, raw_defense, raw_offense):
        self.type_id = type_id
        self.name = name
        self.raw_defense = raw_defense
        self.raw_offense = raw_offense            
    
    ###########################################################################    
    def __str__(self):
        return "The {} Type".format(self.name)
    
    def __repr__(self):
        return self.name

###############################################################################
## Practical Typings ##########################################################
###############################################################################
class Typing():
    def __init__(self, ptype, stype):
        self.ptype_heavy = ptype
        self.stype_heavy = self.stype_handle(stype)
        self.ptype = self.ptype_heavy.name
        self.stype = self.stype_heavy.name           
        self.types = [self.ptype, self.stype]
                    
        self.offensive_raw = self.get_effectiveness('Offense') # Where you are attacking others, the effectiveness of your STAB types
        self.defensive_raw = self.get_effectiveness('Defense') # Where others are attacking you, the effectiveness of their STAB Types
    
    ###########################################################################
    def see(self, org):
        a = {'resist':    [i[0] for i in self.defensive_raw if i[1] < 1],
             'weak':      [i[0] for i in self.defensive_raw if i[1] > 1],
             'walled':    [i[0] for i in self.offensive_raw if i[1] < 1],
             'cover':     [i[0] for i in self.offensive_raw if i[1] > 1],
             'immune':    [i[0] for i in self.defensive_raw if i[1] == 0],
             'no effect': [i[0] for i in self.offensive_raw if i[1] == 0]}
        
        return a.get(org)
    
    ###########################################################################
    def gaps(self, pos):
        b = {'not covered': [e for e in t if e not in self.see('cover')],
             'not resisted': [e for e in t if e not in self.see('resist')]}
        
        return b.get(pos)

    ###########################################################################    
    def get_effectiveness(self, output):
        do = self.ptype_heavy.raw_defense
        oo = self.ptype_heavy.raw_offense
        dt = self.stype_heavy.raw_defense
        ot = self.stype_heavy.raw_offense
         
        array = []
        if output == 'Defense':          
            for i in do:
                for e in dt:
                    if i[0] == e[0]:
                        array.append([i[0], i[1] * e[1]])
                    
        elif output == 'Offense':
            for i in oo:
                for e in ot:
                    if i[0] == e[0]:
                        array.append([i[0], max(i[1], e[1])])
                        
        array.sort(key = lambda x: x[0])
        return array
    
    ###########################################################################
    def typing_modify(self, mod, energy, stance = 'defense'):
        s = {'defense': self.defensive_raw,
             'offense': self.offensive_raw}
        
        x = s.get(stance)
        for i in range(18):
            if x[i][0] == energy:
                x[i][1] *= mod
    
    ###########################################################################
    def get_coverage(self):
        coverage = []
        for q in all_types:
            for i in self.see('weak'):    
                if i in q.covers and i not in self.types:
                    coverage.append(q.name)
                    coverage.append(q.name)
                    
            for i in self.see('walled'):
                if i in q.covers:
                    coverage.append(q.name)
                    
            for i in self.gaps('not covered'):
                if i in q.covers:
                    coverage.append(q.name)

        return coverage
    
    ###########################################################################
    def tcheck(self, e, check = 'stab'):
        compare = {'stab': self.types,
                   'need': self.get_coverage()}
        
        return e in compare.get(check)
    
    ###########################################################################    
    def stype_handle(self, given):
        out = {True: no_type,
               False: given}
        
        return out.get(given is False)

###############################################################################
## Data Generation ############################################################        
###############################################################################
all_types = []
for key in defense_dict:
    ET = Energy_Type(key, t[key], defense_dict[key], offense_dict[key])
    all_types.append(ET)
    
no_type = Energy_Type('255', 'No Type', [[i, 1] for i in t], [[i, 0] for i in t])

###############################################################################
## Quick Check ################################################################
###############################################################################
if __name__ == "__main__":
    
    first_type = type_check("Type 1 >> ")
    second_type = type_check("Type 2 >> ")
    
    title = '-'*10
    print('{}Deffensive Ability{}'.format(title, title))    
    for i in defense_calculator(first_type, second_type):
        print(i[0] + ": " + str(i[1]))
    
    print('\n{}Offensive Ability{}'.format(title, title))    
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
        