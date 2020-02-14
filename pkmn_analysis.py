# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 06:30:59 2019

@author: Devlin
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

import UNESCO as un
import table_gen3 as tg
import pkmn_types as pet
import pkmn_move_class as pmc 
import pkmn_strategy as sgy
import pkmn_toolkit as kit
                       
###############################################################################
##############################################################################<
### CHOOSE YOUR OWN ADVENTURE!! ###############################################\
### Choices >> moves, typing, Move-Effects, robust, weak #######################\
#################################################################################\
analysis = 'algo-balance'                                   #|||||||||||||||||||||||||||||||||
#################################################################################/
### Choices >> d-class, evolution, algo-balance ################################/
###############################################################################/
## Analysis on move damage distribtion #######################################<
###############################################################################
if analysis == 'moves': #######################################################
    ###########################################################################
    # Excluding Z moves and Signature moves ### Because they're outliers, duh #
    ###########################################################################
    mpull = kit.SQL_pull('*', 'moves', 'is_z = 0 AND signature = 0')
    base = [pmc.Move(*i) for i in mpull]    
    def move_means(d_class):
        if d_class == 'All':
            subject_moves = [move for move in base if not move.status()]
        else:
            subject_moves = [move for move in base if move.damage_class == d_class]
        
        subject_ed = [move.average_damage for move in subject_moves]
        subject_mean = np.mean(subject_ed)
        subject_types = {i:[] for i in range(18)}

        for move in subject_moves:
            subject_types[move.move_type_id].append(move)

        subject_means = ['' for i in range(18)]
        for key in subject_types:
            expected_damages = [move.average_damage for move in subject_types[key]]
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
    all_rows = [i.upper() for i in kit.type_list]
    damage_table = tg.Table(all_rows, damage_classes, move_data, summary)
    print(damage_table)
#--\### Mean Expected Damage is distributed uniformly accross type so its not a 
#---\## significant factor in type selection ASSUMING every type has an equal 
#----\# offensive presence       
#----|###############################################\
#----\#---------------------------------------------# \
#     #|           |    All |  Physical |  Special |#  \
#     #|-----------|--------|-----------|----------|#   \ 
#     #|    NORMAL |  63.93 |     65.19 |    59.38 |#\   \
#     #|  FIGHTING |   65.8 |     66.53 |     60.0 |#_\   \ 
#     #|    FLYING |  75.33 |     76.82 |    71.25 |#__\   \
#     #|    POISON |  65.33 |     64.17 |    66.11 |#___\   \
#     #|    GROUND |   65.0 |      68.0 |     57.5 |#____\   \
#     #|      ROCK |  80.82 |     83.23 |     70.0 |#_____\   \
#     #|       BUG |  66.82 |     70.37 |     59.0 |#______\   \
#     #|     GHOST |  58.64 |     62.86 |    51.25 |#_______\   \
#     #|     STEEL |  54.23 |     50.91 |     72.5 |#________\   \
#     #|      FIRE |  88.64 |     79.29 |     93.0 |#_________\   \
#     #|     WATER |  76.84 |     73.12 |    78.96 |#__________\   \
#     #|     GRASS |  78.65 |     78.09 |    79.17 |#___________\   \
#     #|  ELECTRIC |  66.67 |      63.0 |     68.5 |#____________\   \
#     #|   PSYCHIC |  66.79 |      70.0 |    65.91 |#_____________\   \
#     #|       ICE |  66.82 |     62.72 |     70.0 |#______________\   \
#     #|    DRAGON |   74.7 |      86.4 |     63.0 |#_______________\   \
#     #|      DARK |  56.32 |     53.12 |    73.33 |#________________\   \
#     #|     FAIRY |  65.83 |      90.0 |     61.0 |#_________________\   \ 
#     #|-----------|--------|-----------|----------|#__________________\   \
#     #|           |  68.45 |     67.33 |    70.26 |#___________________\   \
#    /#---------------------------------------------#\___________________\   \ 
#   /#################################################\___________________\   \
#__/#/#/                                           \#\#\___________________\   \
###########################################################################\\___\
###########################################################################//   /
elif analysis == 'typing':  ##############################################//   /
    #####################################################################//   /
    ## Determining the most effective Defensve and Offensive Type    ###//   /
    ###################################################################//___/   
    def dual_type_skill(stance, output = 'array'):
        dos = {i:[] for i in range(18)}
        m = {True: .75,  # So why is thie necessary?
             False: 1}   # Because just adding the effs overvalues SE damage
    
        for i in pet.all_types:
            for s in pet.all_types:
                skill = []
                if stance == 'defense':
                    for e in pet.defense_calculator(i, s):
                        skill.append(e[1] * m[e[1] == 2])
                
                elif stance == 'offense':
                     for e in pet.offense_calculator(i, s):
                         skill.append(e[1] * m[e[1] == 2])

                dos[pet.all_types.index(i)].append(sum(skill))
                
        best = []
        for key in dos:            
            top = {True: min(dos[key]),
                   False: max(dos[key])}
            
            k = top[stance == 'defense']
            d = dos[key].index(k)
            j = kit.type_list[d]
            p = '{}/{}'.format(kit.type_list[key], j)
            best.append([p, k])
        
        final = [[kit.type_list[key], sum(dos[key])] for key in dos]
        final.sort(key = lambda x: x[1])
        
        best.sort(key = lambda x: x[1])       
        
        out = {'array': final,
               'combos': best}
        
        return out[output]
    
    defense = dual_type_skill('defense')
    kit.paired_print([x[0] for x in defense], [x[1] for x in defense], '>', '<')
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
    kit.paired_print([i[0] for i in offense], [i[1] for i in offense], '.')   ###\    /
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
    v = [e for l in kit.SQL_pull('effect_id', 'moves') for e in l]
    un.sorted_hbar_gen(data = v, title = 'Pure Distribution of Move Effects')
    
    ## Counting Practical Effect Distribution #################################
    moves = []
    array = [i for l in kit.SQL_pull('pkmn_id', 'pokemon') for i in l]
    for pid in array:
        s = kit.SQL_pull('moves', 'strategies', 'pkmn_id = "{}"'.format(pid))
        ccnt = s[0][0]
        moves.append(kit.splint(ccnt))

        
    aggregate = [m for l in moves for m in l]
    x = []
    for i in aggregate:
        effect = kit.SQL_pull('effect_id', 'moves', 'move_id = "{}"'.format(i))[0]
        x.append(effect[0])
        
    un.sorted_hbar_gen(data = x, title = 'Actual Distribution of Move Effects')

###############################################################################\    
## Move Type Weights ###########################################################|             
###############################################################################/  
elif analysis == 'robust':
    strats = kit.SQL_pull('*', 'strategies')
    done = len(strats)
    algo_sets = []
    for s in range(done):
        subject = strats[s]
        target = sgy.Strategy(*subject)
        algo_sets.append(target.algo_moveset)
        print('|'*40)
        print('\n{}/{}     {}%\n'.format(s + 1, done, round((s + 1)/done * 100, 2)))

    a = [[m.move_type.name for m in l if not m.status()] for l in algo_sets]
    d = kit.flat_count(a)
    e = [i[0] for i in d]
    h = kit.create_props(d)
    
    print('Final Proportions')
    kit.paired_print(e, h, '.', ' ', 100)

    j = [[move.name for move in b] for b in algo_sets]
    o = kit.flat_count(j)
    top = 20
    q = o[:top]
    kit.paired_print([i[0] for i in q], [i[1] for i in q], char = '=')
        
    ##  Proportions   ####
    ##  Ground        12.4  <- 12.4% of all moves are ground
    ##  Fighting .... 11.0     as we see bellow, there are 803 instances of 
    ##  Rock          10.4     earthquake among all the algo sets
    ##  Fire ........ 6.3      803/11912 is ~.06 or half of all ground moves
    ##  Normal        6.1  
    ##  Ice ......... 5.7  
    ##  Dark          5.7  
    ##  Poison ...... 5.3      Remember this does not account for status moves
    ##  Grass         4.8      as the type of a status move rarely matters. We
    ##  Bug ......... 4.8      see here that the prime attacking types are ground
    ##  Psychic       4.7      fighting, rock, and fire. flying, fairy, and 
    ##  Water ....... 4.7      dragon suffer from poor distribtion or poor  
    ##  Steel         4.2      coverage or both
    ##  Electric .... 3.4
    ##  Ghost         3.0  
    ##  Flying ...... 2.8
    ##  Fairy         2.3  
    ##  Dragon ...... 2.1  <- least common type
    #####################
    
    ### Most Common Moves ### 
    ##  Earthquake      803    <- duh
    ##  Substitute ==== 542    <- algorithm is fond of putting this on walls
    ##  Swords Dance    462    <- duh
    ##  Ice Beam ====== 352  
    ##  Rock Slide      324  
    ##  Calm Mind ===== 261  
    ##  Psychic         257  
    ##  Return ======== 241  
    ##  Poison Jab      220  
    ##  Work Up ======= 205   <- this is frustrating but I guess its the best
    ##  Roost           200      stat boost most unevolved pkmn get
    ##  Shadow Ball === 192  
    ##  Roar            191   <- really tried my best to get rid of this, but  
    ##  Stone Edge ==== 190      it just wasn't going anywhere
    ##  Flamethrower    174  
    ##  Brick Break === 170  
    ##  Scald           156  
    ##  Focus Blast === 155  
    ##  Toxic           152  
    ##  Energy Ball === 151  
    #########################
    
## Weaknesses and Resistences #################################################
###############################################################################
if analysis == 'weak':
    pkmn = kit.SQL_pull('*', 'pokemon')
    done = len(pkmn)
    weak_raw = []
    resist_raw = []
    for p in range(done):
        subject = pkmn[p]
        target = sgy.Pokemon(*subject)
        typing = pet.Typing(target.ptype, target.stype)
        weak_raw.append(typing.see('weak'))
        resist_raw.append(typing.see('resist'))
    
    weak_data = kit.flat_count(weak_raw)    
    weak_types = [i[0] for i in weak_data]
    weak_props = kit.create_props(weak_data)
    weak_types.append('Normal')
    weak_props.append(0)
    
    resist_data = kit.flat_count(resist_raw)
    resist_types = [i[0] for i in resist_data]
    resist_props = kit.create_props(resist_data)
    
    kit.paired_print(weak_types, weak_props, m = 100)
    print('-'*20)
    kit.paired_print(resist_types, resist_props, char = '=', m = 100)
                
    weak_counts = []
    resist_counts = []
    types_raw = kit.SQL_pull('ptype_index, stype_index', 'pokemon')
    typings = []
    for pair in types_raw:
        a, b = pair
        ptype = pet.all_types[a]
        if b == 255:
            stype = pet.no_type
        else:
            stype = pet.all_types[b]
            
        typings.append(pet.Typing(ptype, stype))
        
    for y in kit.type_list:
        r_count = 0
        w_count = 0
        for pkmn in typings:
            if y in pkmn.see('weak'):
                w_count += 1
            
            if y in pkmn.see('resist'):
                r_count += 1
                
        weak_counts.append(round(w_count/906, 3))
        resist_counts.append(round(r_count/906, 3))
    
    weak_final = kit.t_order(weak_types, weak_props)
    resist_final = kit.t_order(resist_types, resist_props)
    
    type_table = tg.Table(kit.type_list, ['All Weak %', 'All Resist %', 'PKMN Weak %', 'PKMN Resist %'], [weak_final, resist_final, weak_counts, resist_counts])
    print(type_table)

## FINAL DATA
#   ---------------------------------------------------------------------------
#   |           |        % total for all pkmn |                 % of all pkmn |
#   ---------------------------------------------------------------------------
#   |           |  All Weak % |  All Resist % |  PKMN Weak % |  PKMN Resist % |
#   |-----------|-------------|---------------|--------------|----------------|
#   |    Normal |           0 |         0.042 |          0.0 |           0.19 |
#   |  Fighting |       0.077 |         0.079 |        0.252 |          0.355 |
#   |    Flying |       0.073 |         0.036 |        0.237 |          0.162 |
#   |    Poison |       0.039 |         0.063 |        0.128 |          0.286 |
#   |    Ground |        0.08 |         0.054 |         0.26 |          0.245 |
#   |      Rock |       0.083 |         0.037 |        0.269 |          0.166 |
#   |       Bug |       0.062 |         0.064 |        0.203 |          0.288 |
#   |     Ghost |       0.044 |         0.052 |        0.145 |          0.234 |
#   |     Steel |        0.04 |         0.068 |         0.13 |          0.307 |
#   |      Fire |       0.079 |         0.069 |        0.257 |          0.309 |
#   |     Water |       0.055 |         0.064 |         0.18 |           0.29 |
#   |     Grass |        0.06 |         0.096 |        0.195 |          0.432 |
#   |  Electric |       0.067 |         0.064 |        0.219 |          0.288 |
#   |   Psychic |       0.039 |         0.048 |        0.126 |          0.214 |
#   |       Ice |        0.09 |          0.06 |        0.292 |          0.268 |
#   |    Dragon |        0.02 |         0.026 |        0.065 |          0.118 |
#   |      Dark |       0.044 |         0.037 |        0.145 |          0.166 |
#   |     Fairy |       0.048 |         0.042 |        0.158 |          0.188 |
#   ---------------------------------------------------------------------------

## Damage Class Proportions By Type ###########################################
###############################################################################
elif analysis == 'd-class':
    strats = kit.SQL_pull('*', 'strategies')
    done = len(strats)
    algo_sets = []
    for s in range(done):
        subject = strats[s]
        target = sgy.Strategy(*subject)
        algo_sets.append(target.algo_moveset)
        print('|'*40)
        print('\n{}/{}     {}%\n'.format(s + 1, done, round((s + 1)/done * 100, 2)))

    as_flat = [t for l in algo_sets for t in l]
    
    physical = []
    special = []
    for y in kit.type_list:
        vals = {'Physical' : 0,
                'Special': 0,
                'Status': 0}
        for m in as_flat:
            if m.move_type.name == y:
                vals[m.damage_class] += 1
                
        physical.append(vals['Physical'])
        special.append(vals['Special'])
        
    counts_table = tg.Table(kit.type_list, ['Physical', 'Special'], [physical, special])  
    print(counts_table)   
    
    total = sum(physical) + sum(special)
    p_props = [round(i / total, 3) for i in physical]
    s_props = [round(i / total, 3) for i in special]
    desc = [round(sum(p_props), 3), round(sum(s_props), 3)]
    
    props_table = tg.Table(kit.type_list, ['Physical', 'Special'], [p_props, s_props], desc)
    print(props_table)
        
########## Move Type Counts By Damage Class ###
##\______/------------------------------------#
##/      \|           |  Physical |  Special |# 
##\______/|-----------|-----------|----------|#
##/      \|    Normal |       408 |       61 |#
##\______/|  Fighting |       667 |      183 |#
##/      \|    Flying |       111 |      108 |#
##\______/|    Poison |       254 |      153 |#
##/      \|    Ground |       890 |       68 |#
##\______/|      Rock |       722 |       82 |#
##/      \|       Bug |       286 |       81 |#
##\______/|     Ghost |        34 |      195 |#
##/      \|     Steel |       225 |      100 |#
##\______/|      Fire |       122 |      361 |#
##/      \|     Water |       142 |      221 |#
##\______/|     Grass |       136 |      235 |#
##/      \|  Electric |        99 |      166 |#
##\______/|   Psychic |        34 |      331 |#
##/      \|       Ice |        87 |      355 |#
##\______/|    Dragon |        98 |       63 |#
##/      \|      Dark |       306 |      135 |#
##\______/|     Fairy |        56 |      124 |#
##/      \------------------------------------#
###############################################            
##        ------------------------------------
##        |           |  Physical |  Special |
##        |-----------|-----------|----------|
##        |    Normal |     0.053 |    0.008 |
##        |  Fighting |     0.087 |    0.024 |
##        |    Flying |     0.014 |    0.014 |
##        |    Poison |     0.033 |     0.02 |
##        |    Ground |     0.116 |    0.009 |
##        |      Rock |     0.094 |    0.011 |
##        |       Bug |     0.037 |    0.011 |
##        |     Ghost |     0.004 |    0.025 |
##        |     Steel |     0.029 |    0.013 |
##        |      Fire |     0.016 |    0.047 |
##        |     Water |     0.018 |    0.029 |
##        |     Grass |     0.018 |    0.031 |
##        |  Electric |     0.013 |    0.022 |
##        |   Psychic |     0.004 |    0.043 |
##        |       Ice |     0.011 |    0.046 |
##        |    Dragon |     0.013 |    0.008 |
##        |      Dark |      0.04 |    0.018 |
##        |     Fairy |     0.007 |    0.016 |
##        |-----------|-----------|----------|
##        |           |     0.607 |    0.395 |
##        ------------------------------------
###############################################
 
## Which Types Are More Likely to Evolve? #####################################    
###############################################################################       
elif analysis == 'evolution': #################################################
    data = kit.SQL_pull('ptype_index, stype_index, evolved', 'pokemon')
    unevolved_types = []
    type_points = []
    for triplet in data:
        p, s, evo = triplet
        ptype = kit.type_list[p]
        type_points.append(ptype)
        if not evo:
            unevolved_types.append(ptype)
            
        if s != 255:
            stype = kit.type_list[s]
            type_points.append(stype)
            if not evo:
                unevolved_types.append(stype)
    
    ue_counts = Counter(unevolved_types)
    uet_sorted = sorted(list(ue_counts.items()), key = lambda x: x[0])
    
    type_counts = Counter(type_points)
    tc_sorted = sorted(list(type_counts.items()), key = lambda x: x[0])
    
    unevolved_props = [round(uet_sorted[i][1] / tc_sorted[i][1], 3) for i in range(18)]
    kit.paired_print(sorted(kit.type_list), unevolved_props, m = 100)
        
      ## Proportion Unevolved ##
      # Bug           49.4     #  So these are the proportions of each type that
      # Dark -------- 44.8     #  are unevolved. We can interpret this as a types
      # Dragon        42.6     #  likelihood to evolve, with steel on the lower
      # Electric ---- 38.3     #  end, 37% of steel types are not yet fully
      # Fairy         45.3     #  evolved, and Poison on the high end, with 56%
      # Fighting ---- 41.9     #  of poison types not yet fully evolved. 
      # Fire          50.0     #
      # Flying ------ 40.4     #
      # Ghost         41.8     #
      # Grass ------- 51.4     #
      # Ground        50.7     #
      # Ice --------- 39.5     # 
      # Normal        47.4     #
      # Poison ------ 56.3     #
      # Psychic       39.4     #
      # Rock -------- 45.6     #
      # Steel         37.3     #
      # Water ------- 48.6     #
      ##########################   
      
### Me, Checking My Work ######################################################      
###############################################################################      
elif analysis == 'algo-balance':
    mpull = kit.SQL_pull('*', 'moves')
    moves = [pmc.Move(*i) for i in mpull]

    status = [move for move in moves if move.status()]
    damage = [move for move in moves if not move.status()]

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
    print(a)
    
    bulk_damage = []
    bulk_status = []
    for m in moves:
        for key in m.specialized_score:
            s = m.specialized_score[key]
            if m.status():
                bulk_status.append(s)
            else:
                bulk_damage.append(s)
                
    bulk = [bulk_status, bulk_damage]
    plt.figure(figsize = (8, 8))
    plt.violinplot(bulk)
    plt.show()
    
    peak_pkmn = (max(bulk_damage), max(bulk_status))
    for m in moves:
        for key in m.specialized_score:
            if m.specialized_score[key] in peak_pkmn:
                print(m, key, peak_pkmn)

## P-SWEEP IRON FIST CONKELDUR FOCUS PUNCH: 371
## ALL DARMANITAN STRATS BELLY DRUM: 227
###############################################################################\
##### Resultant Data ###########################################################\    
#    --------------------------------           The algorithm balances scores  \#\ 
#    |         |   Status |  Damage |        fairly well. Status scores have    \#\
#    |---------|----------|---------|        lower scores on average because I   \#\
#    |     Min |        0 |       0 |        don't want them beating out damaging \#\
#    |    Mean |   50.431 |  58.064 |        moves for spots in the moveset. Also  \#\
#    |  Median |   55.217 |  61.804 |        a lot of status moves are just crap.  /#/
#    |     Max |   157.25 | 201.478 |        I have vmod in tookit for keeping    /#/
#    |     STD |   40.252 |  38.239 |        scores above zero.                  /#/
#    --------------------------------                                           /#/
###############################################################################/#/
################################################################################/
## General Stats ##############################################################/
## 171 possible type combos
## 146 used
##  25 unused type combos