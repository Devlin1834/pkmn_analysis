# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 08:52:06 2019

@author: Devlin
"""

import table_gen3 as tg
import pkmn_types as pet
import pkmn_strategy as sgy
import os
import csv
import numpy as np
from collections import Counter
###############################################################################
#### Raw Data #################################################################
###############################################################################
## I should say thank you to veekun and the pokedex project for supplying all
## the data I have used in this project. I reorganized it to suit my own needs
## and added the basic info for gen 8 pokemon, but without their hard work,
## this would be an exercise in dreaming. 
## Not to imply that what is here is anything spectacular; I mostly just look
## at it and say "...but why?" But it was fun to write and for that I owe
## him/her a thank you. Thanks
################################################################################

refference = list(csv.reader(open("...\\pokemon.csv")))
all_pkmn = [sgy.Pokemon(*i) for i in refference] # 1005 Pokemon Here
complete_pkmn = [pkmn for pkmn in all_pkmn if pkmn.gen != "8"] # 906 Pokemon Here
final_evos = [pkmn for pkmn in complete_pkmn if not pkmn.legendary and pkmn.evolved] # 386 Pokemon Here
viable = [pkmn for pkmn in complete_pkmn if pkmn.evolved or pkmn.is_mega] # 527 Pokemon Here

###############################################################################
#### Team Builder #############################################################
###############################################################################
def team_builder(legals):
    species = [pkmn.name.lower() for pkmn in legals]
    monsters = []
    mega_available = max([pkmn.is_mega for pkmn in legals])
    megas = [pkmn.name.lower() for pkmn in legals if pkmn.can_mega]
    
    for i in range(6):
        print("\nPokemon " + str(i + 1))
        while True:
            name = input("Name: ").lower()
            if name not in species:
                print("That's not a pokemon\nCheck your speeling and try again")
            else:
                break
               
        if name in megas and mega_available:
            use_mega = input('Use {}\'s Mega-Evolution?  >> '.format(name.capitalize())).lower()
            if 'y' in use_mega:
                if name in ['charizard', 'mewtwo']:
                    choice = input('Specify X or Y >> ').lower()
                    if choice in ['x', 'y']:
                        l = ' ' + choice
                    else:
                        l = ' x'
                else:
                    l = ''
                name = 'mega ' + name + l

        monster = pet.selectro(all_pkmn, name)
        if monster.name == 'silvally' or monster.name == 'arceus':
            new_type = pet.type_check("Pick a Type >> ")
            dex = pet.t.index(new_type)
            monster.ptype = pet.all_types[dex]
                  
        m_sets = monster.get_strategies()
        cap = len(m_sets)
        print('{} can run the following sets:'.format(monster.name))
        for s in range(cap):
            print('{}:  {} - Score {}'.format(s + 1, m_sets[s].name, m_sets[s].strategic_score))
            
        print('Please input the number of the set you wish to run')
        while True:
            n = input('>> ')
            if n not in [str(i) for i in range(1, cap + 1)]:
                print('Not an acceptable response, please try again\n')
            else:
                chosen = int(n) - 1
                monster.build = m_sets[chosen]
                break
       
        monsters.append(monster)
        mega_available = not max([pkmn.is_mega for pkmn in monsters])
        if not mega_available:
            legals = [pkmn for pkmn in legals if not pkmn.is_mega]
        monster.print_statblock(view = chosen)
        input('\nCONTINUE?')
        os.system('cls')
                       
    return monsters

###############################################################################
#### The Team Calculator ######################################################
###############################################################################
## The Obvious Weaknesses of this STRATEGIES method is the inability to fully
## implement held items, which can drastically affect things. I maintain that
## this weakness is negated by the fact that any pokemon can hold any item, 
## making item-choice a pure addon, not a requirement for strategic consideration.
## When comparing two pokemon, their typing, movepool, stats, and abilities are
## important to consider, as those make them unique.
##
## The important counterargument is that Mega-Evolutions gain power in the above
## categories by sacrificing the use of a held item, so that will have to be factored
## in somehow. Without knowing the degree to which a pokemon gains by holding an
## item, we can't truly say what is gained or lost by running a mega instead. 
###############################################################################
def team_calculator(team):
    """Take 6 pokemon and see how they work together. This measues team synergy
       not team effectiveness or strategy. It also gives a numeric approach to
       find the weaker links in a team. It will never be able to accurately
       recognise strategy."""
    
    NAMES = [pkmn.name.upper() for pkmn in team]
    builds = [pkmn.build for pkmn in team]
    
    ## Typing Synchronicity ###################################################
    ###########################################################################
    covers = [strat.typing.see('cover') for strat in builds]
    resists = [strat.typing.see('resist') for strat in builds]
    walled = [strat.typing.see('walled') for strat in builds]
    weak = [strat.typing.see('weak') for strat in builds]
    
    all_cover = [t for l in covers for t in l]
    all_resists = [t for l in resists for t in l]
    all_weak = [t for l in weak for t in l]
        
    team_holes = [q for q in sgy.pet.t if q not in all_cover]
    no_wall = [q for q in sgy.pet.t if q not in all_resists]
    no_weak = [q for q in sgy.pet.t if q not in all_weak]

    cover_counted = Counter(all_cover)
    resists_counted = Counter(all_resists)
    weak_counted = Counter(all_weak)

    for q in no_weak:
        weak_counted[q] = 0

    for q in team_holes:
        cover_counted[q] = 0
    
    for q in no_wall:
        resists_counted[q] = 0
       
    scores = []
    for i in range(6):
        good = len(covers[i]) + len(resists[i])
        bad = len(weak[i])
    
        for p in covers[i]:
            good += 1 / cover_counted[p]
    
        for p in resists[i]:
            good += 1 / resists_counted[p]
            
        for p in weak[i]:
            bad += 1 / weak_counted[p]
    
        scores.append(round(good/max(1, bad), 2))
        
    ## Role Synchronicity #####################################################
    ########################################################################### 
    nat_roles = [strat.role for strat in builds]
    
    det_roles_start = [pkmn.get_role_array() for pkmn in team]
    for i in range(6):
        for v in det_roles_start[i]:
            v.insert(2, i)
    
    det_role_scores = [t for l in det_roles_start for t in l]
    roles_sorted = sorted(det_role_scores, key = lambda x: x[1], reverse = True)
    roles_copy = roles_sorted.copy()
    
    det_roles = ['???' for i in range(6)]
    used = []
    while '???' in det_roles:
        up = roles_sorted[0]
        det_roles[up[2]] = up[0]
        used.append(up[2])
        used.append(up[0])
        for i in roles_copy:
            try:
                if i[2] in used or i[0] in used:
                    roles_sorted.remove(i)
            except ValueError:
                pass

    ## Stats Synchronicity ####################################################
    ###########################################################################
    stats = [strat.stats_array for strat in builds]
    
    means = [np.mean([s[i] for s in stats]) for i in range(6)]
    bests = []
    for s in range(6):
        detail = [[sgy.base_stats[i], stats[s][i]] for i in range(6)]
        sd = sorted(detail, key = lambda x: x[1], reverse = True)
        bests.append(sd[:2])
        
    stat_scores = []
    for s in range(6):
        top_score = bests[s][0][1]
        top_name = bests[s][0][0]
        runner_up = bests[s][1][1]
        silver_name = bests[s][1][0]
        
        m1 = sgy.base_stats.index(top_name)
        m2 = sgy.base_stats.index(silver_name)
        
        score1 = (top_score / means[m1])
        score2 = (runner_up / means[m2])
        stat_scores.append(round((score1 + score2 - 2) * 10, 2))
    
    cmod = len(set(all_cover)) * len(all_cover)
    rmod = len(set(all_resists)) * len(all_resists)
    wmod = len(set(all_weak)) * len(all_weak)
    typing_modifier = (cmod + rmod) / wmod
    
    holes_modifier = 0
    if len(team_holes) > 0:
        for i in team_holes:
            if i in all_weak:
                holes_modifier -= .1
    else:
        holes_modifier += .5

    weak_modifier = 0
    if len(no_wall) > 0:    
        for i in no_wall:
            if i in all_weak:
                weak_modifier -= .1
    else:
        weak_modifier += .5   
                
    skill_modifiers = []
    for monster in stats:            
        for i in range(6):
            if i == 0:
                stat = [(2 * (pkmn.base_array[i] + 31)) + 110 for pkmn in final_evos]
            else:
                stat = [(2 * (pkmn.base_array[i] + 31)) + 5 for pkmn in final_evos]
            stat_mean = np.mean(stat)
            stat_sig = np.std(stat)
            z = (monster[i] - stat_mean) / stat_sig
            skill_modifiers.append(z)
    
    skill_modifier = round(sum(skill_modifiers) / 6, 2)
    
    range_modifier = 0
    role_arrays = [pkmn.get_role_array() for pkmn in team]
    dead_weight = []
    for i in range(6):
        subject = role_arrays[i]
        nscore = [s[1] for s in subject if s[0] == nat_roles[i]][0]
        dscore = [s[1] for s in subject if s[0] == det_roles[i]][0]
        dwl = nscore - dscore
        loss = (dwl / 180) * .3
        range_modifier += .3 - loss
        dead_weight.append(dwl)
    
    stat_collections = [[s[i] for s in stats] for i in range(6)]
    stat_averages = [np.mean(c) for c in stat_collections]
    stat_var = [np.var(c) for c in stat_collections]
    final_sigma = np.sqrt(sum(stat_var))
    max_z = (max(stat_averages) - np.mean(stat_averages)) / final_sigma
    min_z = (min(stat_averages) - np.mean(stat_averages)) / final_sigma

    balance_modifier = round((max_z + min_z) * 2.5, 2)
    
    team_score = balance_modifier + range_modifier + typing_modifier + weak_modifier + holes_modifier + skill_modifier

    ## Data Return ############################################################
    ###########################################################################       
    print('\n   --STATS BREAKDOWN--')
    bs_arrays = [pkmn.base_array for pkmn in team]
    stat_totals = [pkmn.bst for pkmn in team]
    stats_table = tg.Table(sgy.base_stats, NAMES, bs_arrays, stat_totals)
    print(stats_table.table)
    
    print('\n   --STATS ANALYSIS--')
    scnames = ['Nat Role', 'Det Role', 'Role Loss', 'St. Dev.', 'Score']
    ind_sigmas = [pkmn.get_std() for pkmn in team] 
    sdata = [nat_roles, det_roles, dead_weight, ind_sigmas, stat_scores]
    sanal_table = tg.Table(NAMES, scnames, sdata)
    print(sanal_table.table)
        
    print('\n   --MOVESET BREAKDOWN--')
    movesets = [[m.name for m in p.algo_moveset] for p in builds]
    move_table = tg.Table(['SLOT {}'.format(i) for i in range(1, 5)], NAMES, movesets)
    print(move_table.table)
        
    print('\n   --TYPING BREAKDOWN--')
    cover_tuples = sorted(list(cover_counted.items()), key = lambda x: x[0])
    wall_tuples = sorted(list(resists_counted.items()), key = lambda x: x[0])
    weak_tuples = sorted(list(weak_counted.items()), key = lambda x: x[0])
    bcnames = ["Covers", "Resists", "Weak"]
    bdata = [[c[1] for c in cover_tuples], [w[1] for w in wall_tuples], [w[1] for w in weak_tuples]]
    breakdown_table = tg.Table([t[0].upper() for t in cover_tuples], bcnames, bdata)
    print(breakdown_table.table)

    print('\n   --TYPING ANALYSIS--')
    covers_summary = [len(x) for x in covers]
    walled_summary = [len(x) for x in walled]
    resists_summary = [len(x) for x in resists]
    weak_summary = [len(x) for x in weak]
    tcnames = ["Covers", "Walled", "Resists", "Weak", "Score"]
    tdata = [covers_summary, walled_summary, resists_summary, weak_summary, scores]
    tanal_table = tg.Table(NAMES, tcnames, tdata)
    print(tanal_table.table)

    print("\nSpecialization:            +  {}".format(skill_modifier))            
    print("Role Fulfilment:           +  {}".format(range_modifier))
    print("Stat Balance:              +  {}".format(balance_modifier))
    print("Type Economy:              +  {}".format(typing_modifier))
    print("Resistence Capability:     +  {}".format(weak_modifier))
    print("Coverage Capability:       +  {}".format(holes_modifier))
    print("\nTEAM SCORE:                   {}".format(team_score))  
    print("\n" + "~~"*50) 
    
###############################################################################
#### If __name__ == '__main__' ################################################
###############################################################################
if __name__ == '__main__':
    final_team = team_builder(complete_pkmn)
    team_calculator(final_team)