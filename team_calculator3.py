# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 08:52:06 2019

@author: Devlin
"""
import pokemon
import table_gen2
import pkmn_class
import csv
import numpy as np
import random as rn
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as sts
from collections import Counter

###############################################################################
#### Function #################################################################
## Refference is the full list of pokemon from pokemon.csv ####################
## Refference is a list of lists. The Sublists are arranged as follows ########
## 0 - Name                                                            ######## 
## 1 - Primary Type                                                    ########
## 2 - Secondary Type                                                  ########  
## 3 - HP                                                              ########
## 4 - ATK                                                             ########
## 5 - DEF                                                             ########
## 6 - SP ATK                                                          ########
## 7 - SP DEF                                                          ########
## 8 - SPD                                                             ########
## 9 - Generation                                                      ########
## 10 - Legendary? TRUE/FALSE                                          ########
## 11 - Fully Evolved? TRUE/FALSE                                      ########
## 12 - Mega-Evolution? TRUE/FALSE                                     ########
###############################################################################
## This Script differentiates itself from team_calculator2 by the inclusion of
## the Pokemon class, which changes a lot of things. Net, it actually adds more
## lines but it makes up for it by improving readability and letting me use 
## classes for once. That being said, let me explain how it works #############
#- all_pkmn is the Pokemon class applied to every line in refference        ###
#- species is a lis of Pokemon names                                        ###
#- viable_mons are all non-legendary, fully-evolved Pokemon                 ###
###############################################################################

refference = list(csv.reader(open("C:\\Users\\Devlin\\Documents\\pokemon.csv")))
all_pkmn = [pkmn_class.Pokemon(*i) for i in refference]
species = [pkmn.name.lower() for pkmn in all_pkmn]
viable_mons = [pkmn for pkmn in all_pkmn if pkmn.legendary == 'FALSE' and pkmn.evolved == 'TRUE']

def team_calculator(team, printout = True):
    """Take 6 pokemon and see how they work together. This measues team synergy
       not team effectiveness or strategy. It also gives a numeric approach to
       find the weaker links in a team. It will never be able to accurately
       recognise strategy."""
    
###############################################################################
#### Type Breakdown ###########################################################
## The Pokemon class does a lot of the early work here. The script gets to work
## almost exclusively on team synergy.
#- NAMES is a list of uppercase names for each pkmn on team
#- The Pokemon class has two functions that interpret the results of the typing
#  calculators from pokemon.py and pokemon_offense.py. They way they interpret
#  the results depends on the arguments passed to it
#       -score returns the sum of the effectiveness
#       -covers returns a list of type-names that get covered
#       -walls, holes, and weak do the same as covers
#- all_  lists are flattened versions of the above
#- the next 3 are types the team doesn't cover, resist, or have a weakness to
#-   _counted are the all_  lists with collections.Counter applied
###############################################################################
#### Score Calculation ########################################################
## Each pokemon gets a score based on their typing ############################
## That score is equal to the number of types they cover + the number of types
## they resist all divided by the number of types they're weak to.
## Each pokemon gets a score bonus based on how many other pokemon on team 
## cover or resist the same types as them. ####################################
###############################################################################
    
    NAMES = [pkmn.name.upper() for pkmn in team]
    
    deffense_summary = [pkmn.get_deffensive_ability('score') for pkmn in team]
    offense_summary = [pkmn.get_offensive_ability('score') for pkmn in team]
    
    covers = [pkmn.get_offensive_ability('covers') for pkmn in team]
    walls = [pkmn.get_deffensive_ability('walls') for pkmn in team]
    holes = [pkmn.get_offensive_ability('holes') for pkmn in team]
    weak = [pkmn.get_deffensive_ability('weak') for pkmn in team]
    
    all_cover = [t for l in covers for t in l]
    all_walls = [t for l in walls for t in l]
    all_weak = [t for l in weak for t in l]
        
    team_holes = [q for q in pokemon.t if q not in all_cover]
    team_weak = [q for q in pokemon.t if q not in all_walls]
    no_weak = [q for q in pokemon.t if q not in all_weak]

    cover_counted = Counter(all_cover)
    walls_counted = Counter(all_walls)
    weak_counted = Counter(all_weak)

    # These make sure every type is represented in the dicionaries
    for q in no_weak:
        weak_counted[q] = 0

    for q in team_holes:
        cover_counted[q] = 0
    
    for q in team_weak:
        walls_counted[q] = 0
       
    scores = []
    for i in range(6):
        good = len(covers[i]) + len(walls[i])
        bad = len(weak[i])
    
        for p in covers[i]:
            good += 1/cover_counted[p]
    
        for p in walls[i]:
            good += 1/walls_counted[p]
            
        for p in weak[i]:
            bad += 1/weak_counted[p]
    
        scores.append(round(good/bad, 2))
    
###############################################################################
#### Stats Breakdown ##########################################################
## Natural Roles, Stat Lists, Stat Totals, Stat Deviations are now calculated
## as part of the Pokemon Class, again leaving this script free to focus on
## consolodation and team synergy. The worst part of this section is the 
## loop to determine natural roles but getting stat scores isn't any more fun
###############################################################################
#### Score Calculation ########################################################
## Stat scores are calculated by taking a pokemons highest stat and dividing it
#  by the team average for that stat, doing the same for the second highest,
#  then adding those two together. This number tends to be between 2 and 3, 
#  which makes sense if you think about it, so I subtract 2 and multiply it by
#  10 to make it more dramaic. This has the added benefit of allowing for 
#  negative scores, in the event that a pkmns highest stat is still below
#  average. Interpretation is much easier. ####################################
###############################################################################
   
    stats = [pkmn.stats_array for pkmn in team]
    nat_roles = [pkmn.get_role() for pkmn in team]
    bests = []
    for s in range(6):
        detail = [[pkmn_class.base_stats[i], stats[s][i]] for i in range(6)]
        sd = sorted(detail, key = lambda x: x[1])
        bests.append([sd[-1], sd[-2]])
    
    det_role_scores = []
    roles2 = {'P-SWEEP': [1, 5],       #ATK, SPD
              'P-WALL': [0, 2],        #HP, DEF
              'P-TANK': [1, [0, 2]],   #ATK, [HP or DEF]
              'S-SWEEP': [3, 5],       #SP ATK, SPD
              'S-WALL': [0, 4],        #HP, SP DEF
              'S-TANK': [3, [0, 4]]}   #SP ATK, [HP or SP DEF]
    
    # This loop is convoluted so I'll explain in depth
    # The idea is simple enough, each role is built on two stats
    # so for each pkmn it sums the two stats for each role and adds it to a list
    # Each Key in roles2 is a role
    # Each item is a list of the indexes for the relevant stats for that role
    for key in roles2:
        for i in range(6):
            # Tanks have two varieties that do the same thing
            # The loop evaluate both options and picks the better one
            if type(roles2[key][1]) == list:
                # stats[i][roles2[key][1][0]] - gross
                # roles2[key][1][0] = the first element of the second element in the item for that key
                # it evaluates to an index for the second stat for a tank
                # the index gets fed to stats[i] - the list of stats for pokemon i
                # It then evaluates for the second element in the second element
                # And picks the max between the two, assigned to better
                better = max([stats[i][roles2[key][1][0]], stats[i][roles2[key][1][1]]])
                # Now it evaluates the first element of the item for key
                # This will be the first stat for the role
                # adds it to the stat found for better, assigned to r_score
                r_score = stats[i][roles2[key][0]] + better
                # appends a list of lists role, score, index of pkmn
                det_role_scores.append([key, r_score, i])
            else:
                # Here it does as above but easier
                r_score = stats[i][roles2[key][0]] + stats[i][roles2[key][1]]
                det_role_scores.append([key, r_score, i])
    
    # creating a list of len == 6 lets me assign the role to the same index and its pkmn
    det_roles = ['???' for i in range(6)]
    # sorts based upon r_score
    roles_sorted = sorted(det_role_scores, key = lambda x: x[1])
    # I need a copy to iterate over
    roles_copy = roles_sorted.copy()
    # the list of pokemon who have roles and roles that have pokemon
    used = []
    # While pkmn don't have roles
    while '???' in det_roles:
        # last element in roles_sorted becomes a role
        det_roles[roles_sorted[-1][2]] = roles_sorted[-1][0]
        # The role and pkmn get added to used
        used.append(roles_sorted[-1][2])
        used.append(roles_sorted[-1][0])
        for i in roles_copy:
            # since its a copy and I remove things a lot, it was throwing errors
            try:
                # removes used mons and roles
                if i[2] in used or i[0] in used:
                    roles_sorted.remove(i)
            except ValueError:
                pass

    stat_totals = [str(pkmn.get_bst()) for pkmn in team]
    ind_sigmas = [str(pkmn.get_std()) for pkmn in team] 
    
    means = [np.mean([s[i] for s in stats]) for i in range(6)]
    stat_scores = []
    for s in range(6):
        #bests[s][0][1]
        #      s - the pkmn
        #         0 - the (0 - first), (1 - second) best stat
        #            1 - the (0 - stat name), (1 - stat value)
        # So read as "Pokemon S's First Best Stat divided by the Team Mean for that stat
        score1 = (bests[s][0][1]/means[pkmn_class.base_stats.index(bests[s][0][0])])
        score2 = (bests[s][1][1]/means[pkmn_class.base_stats.index(bests[s][1][0])])
        stat_scores.append(str(((round((score1 + score2 - 2) * 10, 2)))))
    
###############################################################################
#### Score ####################################################################
## The Team Score Modifiers are as follows: ###################################
## TYPING MODIFIER is easy to read. It is the number of types covered total 
#  (meaning if 2 pokemon cover fire, that counts as 2) plus the number of 
#  types resisted by the team (with the same calculation as with covers) all
#  divided by the total number of weaknesses (same rule again)
## HOLES MODIFIER is .5 if the team covers all 18 types. If not, it is -.1 for
#  each type not covered that the team also lacks a resistence to
## WEAK MODIFIER is .5 if the team has a resistence to every type. If not, it
#  is -.1 for each type not resisted that the team also has a weakness to
## SKILL MODIFIER is based on stat values. High level stats get high positive
#  bonuses but low level stats get deductions. 
## RANGE MODIFIER is to make sure as many types as possible are represnted in 
#  claims and seconds. .25 for each unique type in the combind list
## BALANCE MODIFIER is to make sure no one stat is lacking in the team. It is 
#  the Z-Score for the highest and lowest average stat, using the mean of means
#  and the stdev for the means, added together. It will be negative if one stat
#  is significantly lower all around and positive in the inverse
###############################################################################    
    
    typing_modifier = round((len(all_cover)+len(all_walls))/len(all_weak), 2)
    
    holes_modifier = 0
    if len(team_holes) > 0:
        for i in team_holes:
            if i in all_weak:
                holes_modifier -= .1
    else:
        holes_modifier += .5

    weak_modifier = 0
    if len(team_weak) > 0:    
        for i in team_weak:
            if i in all_weak:
                weak_modifier -= .1
    else:
        weak_modifier += .5   
                
    skill_modifiers = []
    for monster in stats:            
        for i in range(6):
            stat = [pkmn.stats_array[i] for pkmn in viable_mons]
            stat_mean = np.mean(stat)
            stat_sig = np.std(stat)
            z = (monster[i] - stat_mean)/stat_sig
            skill_modifiers.append(z)
    skill_modifier = round(sum(skill_modifiers)/6, 2)
    
    range_modifier = 0
    for i in range(6):
        if det_roles[i] == [r.replace('*', '') for r in nat_roles][i]:
            range_modifier += .25
    
    stat_collections = [[s[i] for s in stats] for i in range(6)]
    stat_averages = [np.mean(c) for c in stat_collections]
    stat_var = [np.var(c) for c in stat_collections]
    final_sigma = np.sqrt(sum(stat_var))
    high = max(stat_averages)
    low = min(stat_averages)
    max_z = (high - np.mean(stat_averages))/final_sigma
    min_z = (low - np.mean(stat_averages))/final_sigma

    balance_modifier = round((max_z + min_z) * 2.5, 2)
    
    team_score = balance_modifier + range_modifier + typing_modifier + weak_modifier + holes_modifier + skill_modifier
            
###############################################################################
#### Printout #################################################################
## This section makes use of he above informaion in conjunction with table_gen,
#  a script i wrote to turn lists into tables. table_gen requires everything to
#  to a be string and for the tables contents to be in a list of lists so
#  there's data organization and then a summary of the TEAM SCORE modifiers
###############################################################################
    if printout == True:

        print('\n\n\n   --STATS BREAKDOWN--')
        str_stats = [[str(s) for s in pkmn.stats_array] for pkmn in team]
        table_gen2.table_gen(row_names = pkmn_class.base_stats, col_names = NAMES, list_of_lists = str_stats)
    
        print('\n   --STATS ANALYSIS--')
        scnames = ['Nat Role', 'Det Role', 'BST', 'St. Dev.', 'Score']
        sdata = [nat_roles, det_roles, stat_totals, ind_sigmas, stat_scores]
        table_gen2.table_gen(row_names = NAMES, col_names = scnames, list_of_lists = sdata)
        
        print('\n   --TYPING BREAKDOWN--')
        cover_tuples = sorted(list(cover_counted.items()), key = lambda x: x[0])
        wall_tuples = sorted(list(walls_counted.items()), key = lambda x: x[0])
        weak_tuples = sorted(list(weak_counted.items()), key = lambda x: x[0])
        brnames = [t[0].upper() for t in cover_tuples]
        bcnames = ["Covers", "Resists", "Weak"]
        bdata = [[str(c[1]) for c in cover_tuples], [str(w[1]) for w in wall_tuples], [str(w[1]) for w in weak_tuples]]
        table_gen2.table_gen(row_names = brnames, col_names = bcnames, list_of_lists = bdata)

        print('\n   --TYPING ANALYSIS--')
        covers_summary = [str(len(x)) for x in covers]
        holes_summary = [str(len(x)) for x in holes]
        walls_summary = [str(len(x)) for x in walls]
        weak_summary = [str(len(x)) for x in weak]
        scores_summary = [str(x) for x in scores]
        tcnames = ["Covers", "Holes", "Resists", "Weak", "Score"]
        tdata = [covers_summary, holes_summary, walls_summary, weak_summary, scores_summary]
        table_gen2.table_gen(row_names = NAMES, col_names = tcnames, list_of_lists = tdata)
        
        print("\nBest Offensive Typing: {}".format(NAMES[offense_summary.index(max(offense_summary))]))
        print("Best Deffensive Typing: {}".format(NAMES[deffense_summary.index(min(deffense_summary))]))

        print("\nSpecialization:            +  {}".format(skill_modifier))            
        print("Role Fulfilment:           +  {}".format(range_modifier))
        print("Stat Balance:              +  {}".format(balance_modifier))
        print("Type Economy:              +  {}".format(typing_modifier))
        print("Resistence Capability:     +  {}".format(weak_modifier))
        print("Coverage Capability:       +  {}".format(holes_modifier))
        print("\nTEAM SCORE:                   {}".format(team_score))  
        print("\n" + "~~"*50)  
        
    return team_score
    
###############################################################################
#### If __name__ == '__main__' ################################################
###############################################################################

if __name__ == '__main__':
    monsters = []
    mega = 0
    for i in range(6):
        print("\nPokemon " + str(i+1))
        while True:
            name = input("Name: ")
            if name.lower() not in species:
                print("That's not a pokemon\nCheck your speeling and try again")
            else:
                break
            
        ## This is in lieu of chosen best mega
        ## Since Charizard and Mewtwo get two megas they're a special case
        if 'mega ' + name.lower() in species and mega == 0:
            use_mega = input('Use {}\'s Mega-Evolution?  >> '.format(name.capitalize()))
            if 'y' in use_mega.lower():
                mega_name = 'mega ' + name
                monster = [pkmn for pkmn in all_pkmn if pkmn.name.lower() == mega_name.lower()][0]
                mega += 1
            else:
                monster = [pkmn for pkmn in all_pkmn if pkmn.name.lower() == name.lower()][0]
        elif mega == 0 and name.lower() in ['charizard', 'mewtwo']:
            use_mega = input('Use {}\'s Mega-Evolution? Specify X or Y >> '.format(name.capitalize()))
            if 'y' in use_mega.lower():
                mega_name = 'mega ' + name + ' y'
                monster = [pkmn for pkmn in all_pkmn if pkmn.name.lower() == mega_name.lower()][0]
                mega += 1
            elif 'x' in use_mega.lower():
                mega_name = 'mega ' + name + ' x'
                monster = [pkmn for pkmn in all_pkmn if pkmn.name.lower() == mega_name.lower()][0]
                mega += 1
            else:
                monster = [pkmn for pkmn in all_pkmn if pkmn.name.lower() == name.lower()][0]
        else:
            monster = [pkmn for pkmn in all_pkmn if pkmn.name.lower() == name.lower()][0]
       
        
        # Silvally and Arceus can be any type
        # To allow for this, I let the user specify the type they want
        # This doesn't work with more than one Arceus or Silvally on team
        # It also means that data won't simulate with thier different types
        if monster.name == 'silvally' or monster.name == 'arceus':
            while True:
                new_type = input("Which Type: ").lower()
                if new_type not in pokemon.t:
                    print('Not a real type')
                else:
                    monster.ptype = new_type.capitalize()
                    break
                  
        monsters.append(monster)    
    
    final_score = team_calculator(monsters)
    
###############################################################################
#### Data Simulation and Graphing #############################################
###############################################################################

    scores_data = []
    for i in range(500):
        group = rn.sample(viable_mons, 6)
        scores_data.append(team_calculator(group, printout = False))
        if team_calculator(group, printout = False) > 8:
            print('\nNOTEWORTHY!')
            for g in group:
                print(g[0].capitalize())
    
    viable_sig = np.std(scores_data)
    viable_mean = np.mean(scores_data)
    
    team_z = (final_score - viable_mean)/viable_sig
    prob = 1 - sts.norm.cdf(team_z)
    
    plt.figure(figsize = (8, 8))
    my_plot = sns.distplot(scores_data)
    line = my_plot.get_lines()[-1]
    x, y = line.get_data()
    mask = x > final_score
    x, y = x[mask], y[mask]
    my_plot.fill_between(x, y1 = y, alpha = .5, facecolor = 'red')
    plt.title("Team Z = {}, Probability of Random Replication = {}%".format(round(team_z, 2), round(prob, 2)*100))
    plt.xlabel("Team Scores")
    plt.ylabel("Frequency")
    plt.show()