# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 06:08:23 2019

@author: Devlin
"""

import numpy as np
import table_gen3 as tg3
import pkmn_types as pet
import pkmn_move_class as pmc
import pkmn_toolkit as kit
##|_________________________________________________________________________|##
##| So whats the difference between a pokemon and a strategy? A pokemon is  |##
##| like the wooden hull to a ship. We can add onto it so we can determine  |##
##| what kind of ship it becomes. A pokemon has base stats, up to three     |##
##| abilities, up to two types, and some generic boolean information. On    |##
##| other hand, a strategy takes that one pokemon, picks just one ability   |##
##| picks a role the pokemon's base stats are suited for, then selects EVs, |##
##| IV's, a nature, and moves based on all that information. It uses the    |##
##| types and in some cases the ability to create a typing then algorithmi- |##
##| -cally creates a moveset. Each pokemon can have many strategies.        |## 
##|_________________________________________________________________________|##
###############################################################################
## SECONDARY CLASSES ##########################################################
###############################################################################
class Ability():
    def __init__(self, a_id, name, rb, keywords = 'NA; NA'):
        self.ability_id = a_id
        self.name = name
        self.role_bonus = kit.splint(rb, True)
        self.keywords = kit.splint(keywords)
    
    ###########################################################################
    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.name         

###############################################################################
## BASE POKEMON CLASS #########################################################
###############################################################################
class Pokemon():
    def __init__(self, p_id, base_id, name, ptype, stype, stat_hp, stat_atk, 
                 stat_def, stat_spatk, stat_spdef, stat_spd, gen, legendary, 
                 evolved, is_mega, can_mega, a_ids):
        self.pkmn_id = p_id
        self.base_id = base_id
        
        self.name = name.capitalize()
        self.ptype = pet.all_types[ptype]
        
        if stype == 255:
            self.stype = pet.no_type
        else:
            self.stype = pet.all_types[stype]  
            
        self.base_hp = int(stat_hp)
        self.base_atk = int(stat_atk)
        self.base_def = int(stat_def)
        self.base_spatk = int(stat_spatk)
        self.base_spdef = int(stat_spdef)
        self.base_spd = int(stat_spd)
        self.base_array = [self.base_hp, self.base_atk, self.base_def,
                           self.base_spatk, self.base_spdef, self.base_spd]
        self.bulk = [kit.pull(self.base_array, i) for i in kit.tank]
        self.bst = sum(self.base_array)
        self.stat_std = round(np.std(self.base_array), 2)
        
        self.gen = gen
        self.evolved = evolved
        self.legendary = legendary
        self.is_mega = is_mega
        self.can_mega = can_mega
        
        self.ability_ids = [i for i in kit.splint(a_ids) if i != '']
        
    ###########################################################################
    def get_role_array(self):
        '''calculates all the role scores for this pokemon based on its base stats
        uses role_map in pkmn_toolkit to find each roles target stats and sums
        them. For tanks, uses the maximum from its bulk'''
        role_scores = []
        
        for key in kit.role_map:
            sone = kit.role_map[key][0] 
            stwo = kit.role_map[key][1]
            if type(stwo) is str:
                r_score = self.base_array[sone] + max(self.bulk)
                role_scores.append([key, r_score])
            else:
                r_score = self.base_array[sone] + self.base_array[stwo]
                role_scores.append([key, r_score])
                
        final = sorted(role_scores, key = lambda x: x[1], reverse = True)
        
        return final
    
    ###########################################################################
    def print_statblock(self):
        '''prints a representation of the pokemons stats'''
        print('-'*25)
        print("{}".format(self.name))
        for i in range(6):
            empty = len('SPEED') - len(kit.base_stats[i])
            bar = int(self.base_array[i] / 10)

            
            print("{}{}: {} {}".format(' '*empty, kit.base_stats[i], '|'*bar, self.base_array[i]))
        
        print('-'*25)
        
    ###########################################################################
    def __repr__(self):
        return '{}, Gen {}'.format(self.name, self.gen)
    
    def __str__(self):
        s = {False: '/{}'.format(self.stype.name),
             True: ''}
        
        return '{}, {}{} type from gen {}'.format(self.name, 
                                                  kit.elise(self.ptype.name), 
                                                  s[self.stype.type_id == '255'], 
                                                  self.gen)
        
###############################################################################  
## STRATEGY CLASS #############################################################
###############################################################################
class Strategy():
    def __init__(self, strat_id, name, pkmn_id, mega_id, stat_spread, typing_raw, 
                 a_id, role, moves_raw, nature, ivs, evs):
        self.strat_id = strat_id
        self.name = name
        self.pkmn_id = pkmn_id
        self.mega_id = mega_id
        self.typing = self.read_typing(kit.splint(typing_raw, True))
        self.ability_id = a_id
        self.ability = self.get_ability()
        
        self.role = role
        self.nature = nature
        self.ev_spread = kit.splint(evs, True)
        self.iv_spread = kit.splint(ivs, True)
        self.stats_array = kit.splint(stat_spread, True)
        
        self.move_ids = kit.splint(moves_raw)
        self.moves = self.get_moves()
        self.move_names = [m.name for m in self.moves]
        self.algo_moveset = self.moveset_algorithm()
        
        self.monster = ''
        
    ###########################################################################
    def get_moves(self):
        '''creates an array of move objects'''
        mpull = kit.SQL_pull('*', 'moves', 'move_id IN ({})'.format(', '.join(self.move_ids)))
        return [pmc.Move(*i) for i in mpull]
    
    ###########################################################################
    def get_ability(self):
        '''creates an ability object'''
        apull = kit.SQL_pull('*', 'abilities', 'ability_id = "{}"'.format(self.ability_id))[0]
        return Ability(*apull)
        
    ###########################################################################
    def read_typing(self, raw):
        '''creates a typing based on data pulled from a sqlite table'''
        types = [pet.all_types[t] for t in range(18) if t in raw]
        return pet.Typing(*types)
    
    ###########################################################################    
    def ability_modify(self):
        '''enables abilities to affect a pokemons type effectiveness'''
        for w in self.ability.keywords:
            e = kit.extract(w)
            if 'RESIST' in w or 'IMMUNE' in w:
                m = ('RESIST' in w) * .5
                self.typing.typing_modify(m, e)
            elif 'BUFF' in w:
                b = self.typing.see('weak')
                for q in b:
                    self.typing.typing_modify(.75, q)
            elif 'COVER' in w:
                d = self.typing.defensive_raw
                for i in range(18):
                    if d[i][1] < 1:
                        d[i][1] = 1
            elif 'MIN' in w:
                d = kit.base_stats.index(e)
                self.iv_spread[d] = 0
            elif 'HIT' in w:
                o = self.typing.offensive_raw
                g = [i for i in o if i[0] == 'Ghost'][0]
                g[1] = min(g[1], 1)
        
    ###########################################################################
    def moveset_algorithm(self):
        '''picks the best moves based on the pre-calculated specialized scores
        The specialized Score formula was included in a previous version and
        took a long time to run, hence why I saved all the values to a sqlite
        table. 
        
        The algorithm prevents damaging moves of the same type, status or ailment
        moves of similar effects, or shutting out damaging moves for status 
        moves. If it cannot find another move, it appends celebrate'''
        
        status_lims = {'SWEEP': 1,
                       'TANK': 2,
                       'WALL': 3}
        
        base = sorted(self.moves, key = lambda x: x.specialized_score[self.name], reverse = True)
        moveset = []                
        
        while len(moveset) < 4:
            ccat = [move.category for move in moveset if 'damage' not in move.category]
            ctypes = [move.move_type for move in moveset if not move.status()]
            cstatus = [move for move in moveset if move.status()]
            l = [move for move in base if (move not in moveset) and (move.category not in ccat)]
            l = [move for move in l if (move.move_type not in ctypes) or (move.move_type in ctypes and move.status())]
            if len(cstatus) >= status_lims[self.role[2:]]:
                l = [move for move in l if not move.status()]
            
            added = kit.append_check(moveset, l)
            if not added:
                moveset.append(pmc.celebrate)
                                
        return moveset
    
    ###########################################################################
    def get_score(self):
        '''calculates the strtegic score for this build. score includes...
           m =         Moveset Specialized Score Sum
           role_mods = Type Effectiveness adjusted for role
           x, y =      Final Calculated Stats based on role
           a =         Ability role bonus'''
           
        m = sum([move.specialized_score[self.name] for move in self.algo_moveset])
        o = [e[1] for e in self.typing.offensive_raw]
        d = [e[1] for e in self.typing.defensive_raw]
        for l in [o, d]:
            for p in range(len(l)):
                if l[p] >= 2:
                    l[p] *= .75
        
        s = sum(o) * 20
        w = (40.5 - sum(d)) * 20         
        role_mods = {'SWEEP': s,
                     'WALL': w,
                     'TANK': (s + w) / 2}
        
        sone = kit.role_map[self.role][0]
        stwo = kit.role_map[self.role][1]
        if stwo == 'tank':
            x = max([kit.pull(self.stats_array, i) for i in kit.tank if i != 'HP'])
        else:
            x = self.stats_array[stwo]
            
        y = self.stats_array[sone]
        
        rdex = kit.roles.index(self.role)
        a = self.ability.role_bonus[rdex]
        
        return role_mods[self.role[2:]] + m + x + y + a
        
    ###########################################################################    
    def print_move_analysis(self):
        '''prints all its moves with their specialized scores. Useful for debugging
        and answering the "Why the hell is that move there?" questions'''
        x = sorted(self.moves, key = lambda x: x.specialized_score[self.name], reverse = True)
        for move in x:
            print('{} -- {}'.format(move, move.specialized_score[self.name]))
    
    ###########################################################################       
    def print_type_effectiveness(self):
        '''prints the type effectiveness in a pretty table'''
        o = sorted(self.typing.offensive_raw, key = lambda x: x[0])
        d = sorted(self.typing.defensive_raw, key = lambda x: x[0])
        
        n = [i[0] for i in o]
        c = ['Offensive', 'Defensive']
        a = [[i[1] for i in o], [i[1] for i in d]]
        
        print(tg3.Table(n, c, a))
      
    ###########################################################################
    def __repr__(self):
        return '{}'.format(self.name)
    
    def __str__(self):      
        return '{}: {}'.format(self.name, self.strategic_score)
    
###############################################################################