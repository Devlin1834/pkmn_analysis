# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 06:30:59 2019

@author: Devlin
"""

import numpy as np
import random as rn
import matplotlib.pyplot as plt
from collections import Counter

import UNESCO as un
import table_gen3 as tg
import pkmn_types as pet
import pkmn_move_class as pmc 
import team_calculator5 as tc
###############################################################################
## Since changing over to strategies, it takes too long to collect poplation  
## data, so I base this data on random samples of n = 100 pokemon, and all the
## strategies they run. This means at minimum 100 strategies, but is usually   
## around 250. So take the data given with a grain of salt and know that running
## the scripts yourself will get you different numbers.                       
###############################################################################
##############################################################################<
### CHOOSE YOUR OWN ADVENTURE!! ###############################################\
### Choices >> moves, typing, Move-Effects, robust, weak #######################\
#################################################################################\
analysis = ''                                   #|||||||||||||||||||||||||||||||||
#################################################################################/
### Choices >> d-class, evolution, algo-balance ################################/
###############################################################################/
def flat_count(lol):
    flat = [t for l in lol for t in l]
    counted = Counter(flat)
    ordered = sorted(counted.items(), key = lambda x: x[1], reverse = True)
    
    return ordered

###############################################################################
def create_props(lot):
    data = [i[1] for i in lot]
    total = sum(data)
    
    return [round(i / total, 3) for i in data]

###############################################################################
def paired_print(names, data, char = '-', alt = ' ', m = 1, comment = False):
    if comment:
        p = '#'
        print('#'*20)
    else:
        p = ''
    
    tippy = max(max([len(i) for i in names]) + 2, 12)
    for i in range(len(names)):
        n = tippy - len(names[i])
        if i % 2 == 1:
            bars = char * n
        else:
            bars = alt *n
            
        print('{}  {} {} {}  {}'.format(p, names[i], bars, data[i] * m, p))
        
    if comment:
        print('#'*20)

###############################################################################              
def t_order(names, data):
    x = [''] * 18
    for i in range(18):
        new_dex = pet.t.index(names[i])
        x[new_dex] = data[i]
        
    return x

## Analysis on move damage distribtion ########################################
###############################################################################
if analysis == 'moves': #######################################################
    ###########################################################################
    # Excluding Z moves and Signature moves ### Because they're outliers, duh #
    ###########################################################################
    base = [move for move in pmc.all_moves if move.is_z == False and move.signature == False]    
    def move_means(d_class):
        if d_class == 'All':
            subject_moves = [move for move in base if not move.status()]
        else:
            subject_moves = [move for move in base if move.damage_class == d_class]
        
        subject_ed = [move.expected_damage for move in subject_moves]
        subject_mean = np.mean(subject_ed)
        subject_types = {i:[] for i in range(18)}

        for move in subject_moves:
            subject_types[move.move_type_id].append(move)

        subject_means = ['' for i in range(18)]
        for key in subject_types:
            expected_damages = [move.expected_damage for move in subject_types[key]]
            subject_means[key] = round(np.mean(expected_damages), 2)
            
        return subject_means, subject_mean
    
    ###########################################################################
    # Analysis ################################################################
    move_data = []
    summary = []
    damage_classes = ['All', 'Physical', 'Special']
    for c in damage_classes:
        x = move_means(c)[0]
        y = [str(i) for i in x]
        move_data.append(y)
        
        a = move_means(c)[1]
        b = str(round(a, 2))
        summary.append(b)
        
    ###########################################################################    
    all_rows = [i.upper() for i in pet.t]
    damage_table = tg.Table(all_rows, damage_classes, move_data, summary)
    print(damage_table.table)
#--\### Mean Expected Damage is distributed uniformly accross type so its not a 
#---\## significant factor in type selection ASSUMING every type has an equal 
#----\# offensive presence       
#----|###################################################\
#----\#-------------------------------------------------# \
#     #|            |    All  |  Physical  |  Special  |#  \
#     #|------------|---------|------------|-----------|#   \ 
#     #|    NORMAL  |  57.93  |     59.64  |    51.72  |#\   \
#     #|  FIGHTING  |  60.91  |     62.15  |     51.0  |#_\   \ 
#     #|    FLYING  |  59.14  |     58.35  |    61.31  |#__\   \
#     #|    POISON  |  62.33  |     60.17  |    63.78  |#___\   \
#     #|    GROUND  |  59.65  |     61.76  |    54.38  |#____\   \
#     #|      ROCK  |  66.33  |     65.52  |     70.0  |#_____\   \
#     #|       BUG  |   65.3  |     68.17  |     59.0  |#______\   \
#     #|     GHOST  |  49.09  |     47.86  |    51.25  |#_______\   \
#     #|     STEEL  |  50.13  |     46.95  |    67.62  |#________\   \
#     #|      FIRE  |  79.84  |     76.89  |    81.22  |#_________\   \
#     #|     WATER  |  68.14  |     64.62  |    70.16  |#__________\   \
#     #|     GRASS  |  70.71  |     76.21  |    65.67  |#___________\   \
#     #|  ELECTRIC  |  59.92  |     62.35  |     58.7  |#____________\   \
#     #|   PSYCHIC  |  66.21  |     67.33  |    65.91  |#_____________\   \
#     #|       ICE  |  58.47  |     60.61  |    56.81  |#______________\   \
#     #|    DRAGON  |  69.58  |     78.76  |     60.4  |#_______________\   \
#     #|      DARK  |  55.95  |     53.12  |     71.0  |#________________\   \
#     #|     FAIRY  |  64.33  |      81.0  |     61.0  |#_________________\   \ 
#     #|------------|---------|------------|-----------|#__________________\   \
#     #|            |  62.19  |     61.54  |    63.25  |#___________________\   \
#    /#-------------------------------------------------#\___________________\   \ 
#   /#####################################################\___________________\   \
#__/#/#/                                               \#\#\___________________\   \
###############################################################################\\___\
###############################################################################//   /
elif analysis == 'typing':  ##################################################//   /
    #########################################################################//   /
    ## Determining the most effective Defensve and Offensive Type        ###//   /
    #######################################################################//___/   
    def dual_type_skill(stance, output = 'array'):
        dos = {i:[] for i in range(18)}
        m = {True: .75,  # So why is thie necessary?
             False: 1}   # Because just adding the effs overvalues SE damage
    
        for i in pet.t:
            for s in pet.t:
                skill = []
                if stance == 'defense':
                    for e in pet.defense_calculator(i, s):
                        skill.append(e[1] * m[e[1] == 2])
                
                elif stance == 'offense':
                     for e in pet.offense_calculator(i, s):
                         skill.append(e[1] * m[e[1] == 2])

                dos[pet.t.index(i)].append(sum(skill))
                
        best = []
        for key in dos:            
            top = {True: min(dos[key]),
                   False: max(dos[key])}
            
            k = top[stance == 'defense']
            d = dos[key].index(k)
            j = pet.t[d]
            p = '{}/{}'.format(pet.t[key], j)
            best.append([p, k])
        
        final = [[pet.t[key], sum(dos[key])] for key in dos]
        final.sort(key = lambda x: x[1])
        
        best.sort(key = lambda x: x[1])       
        
        out = {'array': final,
               'combos': best}
        
        return out[output]
    
    defense = dual_type_skill('defense')
    paired_print([x[0] for x in defense], [x[1] for x in defense], char = '>', alt = '<')
    # Defense ####################################################################\
    # Steel <<<<<<< 264.25    Findings:                                         ##|\ 
    # Ghost >>>>>>> 284.25  1) Ghost/Steel is the best Defensive Dual Typing    ##|>\     
    # Poison <<<<<< 300.75  2) Flying/Steel and Fairy/Steel follow              ##|>>>-@ 
    # Fairy >>>>>>> 302.0   3) Ice/Rock is the worse defensive dual typing      ##|>/
    # Water <<<<<<< 302.75                                                      ##|/
    # Electric >>>> 304.25                                                      ##/
    # Fire <<<<<<<< 308.75                                                     ##/ 
    # Normal >>>>>> 310.5                                                     ##/ 
    # Flying <<<<<< 310.5                                                    ##/ 
    # Dragon >>>>>> 316.25                                                   |/
    # Ground <<<<<< 319.25                                                   |
    # Dark >>>>>>>> 319.75                                                   |\
    # Fighting <<<< 323.0                                                    ##\
    # Psychic >>>>> 329.75                                                    ##\
    # Bug <<<<<<<<< 331.25                                                     ##\
    # Grass >>>>>>> 345.25                                                      ##\   
    # Rock <<<<<<<< 350.25                                                      ###\  
    # Ice >>>>>>>>> 361.25                                                      ###/\
    ##############################################################################/  \
                                                                              ###/    \                   
    offense = dual_type_skill('offense')                                       #|>----<|
    paired_print([i[0] for i in offense], [i[1] for i in offense], char = '.')###\    /
    ## Offense ###################################################################\  /
    # Normal        339.0    Findings:                                          ###\/
    # Dragon ...... 349.5  1) Ice/Fighting and Ice Ground are tied for the best ###/\
    # Poison        350.0     Offensive Dual Typing                             ##/\/
    # Grass ....... 353.0  2) Followed by Fairy/Ground                          ##\/\
    # Psychic       356.5                                                       ##/\/  
    # Ghost ....... 357.0                                                       ##\/\
    # Electric      357.5                                                       ##/\/
    # Steel ....... 359.0                                                       ##\/\ 
    # Bug           360.0                                                       ##/\/
    # Dark ........ 360.5                                                       ##\/\
    # Fairy         361.0                                                       ##/\/
    # Flying ...... 362.0                                                       ##\/\ 
    # Water         365.0                                                       ##/\/
    # Ice ......... 367.5                                                       ##\/\ 
    # Fire          369.0                                                       ##/\/
    # Rock ........ 370.5                                                       ##\/\ 
    # Fighting      375.0                                                       ##/\/
   ## Ground ...... 381.5                                                       ##\/
  ################################################################################/         
 ################################################################################/
################################################################################/    
## The Distribution of Move Effect IDs ########################################/
###############################################################################    
elif analysis == 'Move-Effects': ##############################################
    ## WARNING: BOTH OF THESE ARE LONG GRAPHS #################################
    ## they're also boring, but who's honestly gonna run this? ################
    #-------------------------------------------------------------------------#
    ## Counting Raw Effect Distribution #######################################    
    v = [move.effect_id for move in pmc.all_moves]
    un.sorted_hbar_gen(data = v, title = 'Pure Distribution of Move Effects')
    
    ## Counting Practical Effect Distribution #################################
    w = [[move.effect_id for move in p.moves] for p in tc.final_evos]
    x = [t for l in w for t in l]
    un.sorted_hbar_gen(data = x, title = 'Actual Distribution of Move Effects')

################################################################################\    
## Move Type Weights ###########################################################/                   
###############################################################################/  
elif analysis == 'robust':
    sample = rn.sample(tc.viable, 100)
    strats = [pkmn.get_strategies() for pkmn in sample]
    flat_strats = [t for l in strats for t in l]
    a = [[move.move_type.name for move in build.algo_moveset if not move.status()] for build in flat_strats]
    d = flat_count(a)
    e = [i[0] for i in d]
    h = create_props(d)
    
    print('Final Proportions')
    paired_print(e, h, '.', ' ', 100)

    j = [[move.name for move in b.algo_moveset] for b in flat_strats]
    o = flat_count(j)
    top = 20
    q = o[:top]
    paired_print([i[0] for i in q], [i[1] for i in q], char = '=')
        
    ####Final Proportions####
    ##  Rock          14.5 ##  <- The Most Common Type in an Algo Moveset
    ##  Ground ...... 12.5 ## 
    ##  Fighting      7.8  ##
    ##  Ice ......... 6.9  ##
    ##  Dark          6.6  ##
    ##  Water ....... 6.0  ##
    ##  Grass         5.8  ##
    ##  Fire ........ 5.8  ##
    ##  Normal        4.9  ##
    ##  Fairy ....... 4.9  ##
    ##  Bug           4.8  ##
    ##  Flying ...... 4.6  ##
    ##  Electric      3.8  ##
    ##  Poison ...... 3.6  ##
    ##  Steel         2.5  ##
    ##  Psychic ..... 2.5  ##
    ##  Ghost         1.4  ## 
    ##  Dragon ...... 1.3  ##  <- The Least Common Type in an Algo Moveset
    #########################
    
    ### Most Common Moves ### 
    ##  Earthquake        124    There are 435 pokemon in final_evos so over 
    ##  Stone Edge ====== 85     25% of them carry earthquake
    ##  Toxic             59  
    ##  Ice Beam ======== 48  
    ##  Swords Dance      47  
    ##  Roost =========== 44  
    ##  Frustration       37  
    ##  Thunder Wave ==== 37  
    ##  Fire Blast        31  
    ##  Rock Tomb ======= 29  
    ##  Scald             27  
    ##  Agility ========= 26  
    ##  Focus Blast       24  
    ##  Energy Ball ===== 22  
    ##  Dark Pulse        22  
    ##  Frost Breath ==== 22  
    ##  Rock Slide        22  
    ##  Dazzling Gleam == 21  
    ##  Psychic           21  
    ##  Bulk Up ========= 20 
    #########################
    
## Weaknesses and Resistences #################################################
###############################################################################
if analysis == 'weak':
    sample = rn.sample(tc.viable, 100)
    strats = [pkmn.get_strategies() for pkmn in sample]
    
    weak_raw = [build.typing.see('weak') for build in strats]
    weak_data = flat_count(weak_raw)    
    weak_types = [i[0] for i in weak_data]
    weak_props = create_props(weak_data)
    weak_types.append('Normal')
    weak_props.append(0)
    
    resist_raw = [build.typing.see('resist') for build in strats]
    resist_data = flat_count(resist_raw)
    resist_types = [i[0] for i in resist_data]
    resist_props = create_props(resist_data)
    
    paired_print(weak_types, weak_props, m = 100)
    print('-'*20)
    paired_print(resist_types, resist_props, char = '=', m = 100)
                
    weak_counts = []
    resist_counts = []
    for y in pet.t:
        r_count = 0
        w_count = 0
        for pkmn in tc.final_evos:
            if y in pkmn.typing.weak:
                w_count += 1
                
            if y in pkmn.typing.resists:
                r_count += 1
                
        weak_counts.append(round(w_count/435, 3))
        resist_counts.append(round(r_count/435, 3))
    
    weak_final = t_order(weak_types, weak_props)
    resist_final = t_order(resist_types, resist_props)
    
    type_table = tg.Table(pet.t, ['All Weak %', 'All Resist %', 'PKMN Weak %', 'PKMN Resist %'], [weak_final, resist_final, weak_counts, resist_counts])
    print(type_table.table)
    
    ## Weakness Props #####    ## Resistance Props ###
    #  Fighting      8.8  #    #  Grass         8.8  #  Was it difficult to put
    #  Ice --------- 8.3  #    #  Fighting ==== 7.3  #  these two side by side?  
    #  Rock          8.3  #    #  Steel         6.8  #  Yes
    #  Fire -------- 8.2  #    #  Poison ====== 6.5  #  Could I have used table_gen3
    #  Ground        8.2  #    #  Bug           6.4  #  for this?
    #  Flying ------ 7.3  #    #  Fire ======== 6.3  #  Yes, but I didn't think
    #  Electric      6.8  #    #  Ice           6.2  #  of that until just now.
    #  Bug --------- 6.1  #    #  Electric ==== 6.2  #  
    #  Grass         5.9  #    #  Water         6.1  #  This data shows the percent
    #  Water ------- 5.4  #    #  Ghost ======= 5.9  #  of all resistences and
    #  Fairy         4.9  #    #  Ground        5.4  #  weaknesses that each
    #  Steel ------- 4.2  #    #  Psychic ===== 4.9  #  type holds. For example,
    #  Ghost         4.2  #    #  Normal        4.6  #  Ice accounts for 8.3% of
    #  Dark -------- 4.1  #    #  Flying ====== 4.1  #  all weaknesses and 6.2%
    #  Poison        3.9  #    #  Fairy         4.0  #  of all resistances. This 
    #  Psychic ----- 3.7  #    #  Dark ======== 4.0  #  is NOT saying that 6.2%
    #  Dragon        1.6  #    #  Rock          3.7  #  of pokemon resist Ice. 
    #  Normal ------ 0    #    #  Dragon ====== 2.8  #
    #######################    #######################
    
    # Weakenesses of Pokemon ###########
    #----------------------------------#    There, I used table_gen3, are you
    #|            |    W %  |    R %  |#  happy now? So this is the data that
    #|------------|---------|---------|#  most people would have expected above.
    #|    Normal  |      0  |   20.7  |#  28.7% of fully evolved pokemon are 
    #|  Fighting  |   28.7  |   32.9  |#  weak to fighting and 32.9% of them
    #|    Flying  |   23.9  |   18.6  |#  resist or are immune to fighting.
    #|    Poison  |   12.9  |   29.2  |#
    #|    Ground  |   26.7  |   24.4  |#
    #|      Rock  |   27.1  |   16.8  |#
    #|       Bug  |   20.0  |   29.0  |#
    #|     Ghost  |   13.6  |   26.4  |#
    #|     Steel  |   13.8  |   30.8  |#
    #|      Fire  |   26.7  |   28.3  |#
    #|     Water  |   17.5  |   27.4  |#
    #|     Grass  |   19.3  |   39.8  |#
    #|  Electric  |   22.3  |   27.8  |#
    #|   Psychic  |   12.2  |   22.3  |#
    #|       Ice  |   27.1  |   28.0  |#
    #|    Dragon  |    5.3  |   12.6  |#
    #|      Dark  |   13.3  |   17.9  |#
    #|     Fairy  |   16.1  |   17.9  |#
    #----------------------------------#
    ####################################

## Damage Class Proportions By Type ###########################################
###############################################################################
elif analysis == 'd-class':
    sample = rn.sample(tc.viable, 100)
    strats = [pkmn.get_strategies() for pkmn in sample]
    flat_strat = [t for l in strats for t in l]
    algo_sets = [build.algo_moveset for build in flat_strat]
    as_flat = [t for l in algo_sets for t in l]
    
    physical = []
    special = []
    for y in pet.t:
        vals = {'Physical' : 0,
                'Special': 0,
                'Status': 0}
        for m in as_flat:
            if m.move_type.name == y and m.name:
                vals[m.damage_class] += 1
                
        physical.append(vals['Physical'])
        special.append(vals['Special'])
        
    counts_table = tg.Table(pet.t, ['Physical', 'Special'], [physical, special])  
    print(counts_table.table)   
    
    total = sum(physical) + sum(special)
    p_props = [round(i / total, 3) for i in physical]
    s_props = [round(i / total, 3) for i in special]
    desc = [round(sum(p_props), 3), round(sum(s_props), 3)]
    
    props_table = tg.Table(pet.t, ['Physical', 'Special'], [p_props, s_props], desc)
    print(props_table.table)
        
########## Move Type Counts By Damage Class ###        
#        ------------------------------------
#        |           |  Physical |  Special |
#        |-----------|-----------|----------|
#        |    Normal |        39 |        4 |
#        |  Fighting |        59 |       46 |
#        |    Flying |        16 |       24 |
#        |    Poison |        37 |       28 |
#        |    Ground |       139 |       13 |
#        |      Rock |        87 |       24 |
#        |       Bug |        37 |        6 |
#        |     Ghost |         6 |       38 |
#        |     Steel |        28 |       28 |
#        |      Fire |        18 |       67 |
#        |     Water |        17 |       39 |
#        |     Grass |        25 |       40 |
#        |  Electric |        12 |       17 |
#        |   Psychic |         2 |       49 |
#        |       Ice |         5 |       68 |
#        |    Dragon |        19 |       16 |
#        |      Dark |        34 |       18 |
#        |     Fairy |         8 |       17 |
#        ------------------------------------
###############################################
 
## Which Types Are More Likely to Evolve? #####################################    
###############################################################################       
elif analysis == 'evolution': #################################################
    unevolved_types_long = [[y for y in pkmn.typing.types if y != 'No Type'] for pkmn in tc.all_pkmn if not pkmn.evolved]
    unevolved_types = [t for l in unevolved_types_long for t in l]
    all_types_long = [[y for y in pkmn.typing.types if y != 'No Type'] for pkmn in tc.all_pkmn]
    type_points = [t for l in all_types_long for t in l]
    
    ue_counts = Counter(unevolved_types)
    uet_sorted = sorted(list(ue_counts.items()), key = lambda x: x[0])
    
    type_counts = Counter(type_points)
    tc_sorted = sorted(list(type_counts.items()), key = lambda x: x[0])
    
    unevolved_props = [round(uet_sorted[i][1] / tc_sorted[i][1], 3) for i in range(18)]
    paired_print(sorted(pet.t), unevolved_props, m = 100)
        
      ## Proportion Unevolved ##
      # Bug           50.0     #  So these are the proportions of each type that
      # Dark -------- 46.3     #  are unevolved. We can interpret this as a types
      # Dragon        39.7     #  likelihood to evolve, with steel on the lower
      # Electric ---- 36.8     #  end, 35% of steel types are not yet fully
      # Fairy         42.9     #  evolved, and Poison on the high end, with 54%
      # Fighting ---- 40.6     #  of poison types not yet fully evolved. 
      # Fire          51.2     #
      # Flying ------ 40.7     #
      # Ghost         44.4     #
      # Grass ------- 51.3     #
      # Ground        50.0     #
      # Ice --------- 38.5     # 
      # Normal        47.6     #
      # Poison ------ 53.9     #
      # Psychic       40.4     #
      # Rock -------- 45.2     #
      # Steel         35.7     #
      # Water ------- 48.0     #
      ##########################   
      
### Me, Checking My Work ######################################################      
###############################################################################      
elif analysis == 'algo-balance':
    """This takes forever so be prepared"""
    sample = rn.sample(tc.viable, 100)
    long_time = [p.get_strategies() for p in sample]
    status = [move for move in pmc.all_moves if move.status()]
    for move in status:
        move.set_overall_score()

    damage = [move for move in pmc.all_moves if not move.status()]
    for move in damage:
        move.set_overall_score()

    status_scores = [move.overall_score for move in status]
    damage_scores = [move.overall_score for move in damage]
    z = [status_scores, damage_scores]

    plt.figure(figsize = (8, 8))
    plt.violinplot(z)
    plt.show()

    y = ['Min', 'Mean', 'Median', 'Max', 'STD']
    x = [[], []]
    for i in range(2):
        x[i].append(round(min(z[i]), 3))
        x[i].append(round(np.mean(z[i]), 3))
        x[i].append(round(np.median(z[i]), 3))
        x[i].append(round(max(z[i]), 3))
        x[i].append(round(np.std(z[i]), 3))
        
    a = tg.Table(y, ['Status', 'Damage'], x)
    print(a.table)

##### Sample Data ##############################################################\    
#    --------------------------------             Running this script takes so \#\ 
#    |         |   Status |  Damage |        long, that I had to use a random   \#\
#    |---------|----------|---------|        sample to get the data. So the      \#\
#    |     Min |        0 |       0 |        results are a little off, but I      \#\
#    |    Mean |   38.753 |  41.148 |        don't have 23 hours to run strats     \#\
#    |  Median |     50.0 |  39.092 |        for every pokemon so....              /#/
#    |     Max |  169.756 |   160.5 |                                             /#/
#    |     STD |   39.999 |  39.409 |                                            /#/
#    --------------------------------                                           /#/
###############################################################################/#/
################################################################################/
## General Stats ##############################################################/
## 171 possible type combos
## 146 used
##  25 unused type combos

    