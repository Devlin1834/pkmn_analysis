# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 06:08:23 2019

@author: Devlin
"""

import numpy as np
import pokemon
import pokemon_offense

base_stats = ['HP', 'ATK', 'DEF', 'SP ATK', 'SP DEF', 'SPD']

class Pokemon():
    def __init__(self, name, ptype, stype, stat_hp, stat_atk, stat_def, stat_spatk, stat_spdef, stat_spd, gen, legendary, evolved, is_mega, can_mega):
        self.name = name
        self.ptype = ptype
        if stype == '':
            self.stype = False
        else:
            self.stype = stype
        self.stat_hp = int(stat_hp)
        self.stat_atk = int(stat_atk)
        self.stat_def = int(stat_def)
        self.stat_spatk = int(stat_spatk)
        self.stat_spdef = int(stat_spdef)
        self.stat_spd = int(stat_spd)
        self.stats_array = [self.stat_hp, self.stat_atk, self.stat_def, self.stat_spatk, self.stat_spdef, self.stat_spd]
        self.gen = gen
        self.legendary = legendary
        self.evolved = evolved
        self.is_mega = is_mega
        self.can_mega = can_mega
                      
    def get_bst(self):
        return sum(self.stats_array)
    
    def get_std(self):
        return round(np.std(self.stats_array), 2)
    
    def get_min_atk(self):
        return sorted([[self.stat_atk, 1], [self.stat_spatk, 3]])[0][1]
    
    def get_role(self):
        role_l = []
        roles = {"P-WALL": [['HP', 'DEF'], ['DEF', 'HP']],
                 "P-TANK": [['HP', 'ATK'], ['ATK', 'HP'], ['ATK', 'DEF'], ['DEF', 'ATK']],
                 "P-SWEEP": [['ATK', 'SPD'], ['SPD', 'ATK']],
                 "S-WALL": [['HP', 'SP DEF'], ['SP DEF', 'HP']],
                 "S-TANK": [['HP', 'SP ATK'], ['SP ATK', 'HP'], ['SP ATK', 'SP DEF'], ['SP DEF', 'SP ATK']],
                 "S-SWEEP": [['SP ATK', 'SPD'], ['SPD', 'SP ATK']]}
        order = [[1, 2], [1, 3], [1, 4], [2, 3], [1, 5], [2, 4], [1, 6]]
        detail = sorted([[base_stats[i], self.stats_array[i]] for i in range(6)], key = lambda x: x[1])
        draft = 0
        while role_l == []:
            bests = [detail[-order[draft][0]][0], detail[-order[draft][1]][0]]
            role_l = [key for key in roles if bests in roles[key]]
            if role_l == []:
                draft += 1
        role = role_l[0] + '*'*draft
        return role
    
    def get_deffensive_ability(self, output = ''):
        
        ability = pokemon.deffense_calculator(self.ptype, self.stype)
        
        out = {'score': sum([e[1] for e in ability]),
               'walls': [e[0] for e in ability if e[1] < 1],
               'weak': [e[0] for e in ability if e[1] > 1]}
       
        if output in out.keys():
            return out[output]
        else:
            return ability
    
    def get_offensive_ability(self, output = ''):
        
        ability = pokemon_offense.offense_calculator(self.ptype, self.stype)
        
        out = {'score': sum([e[1] for e in ability]),
               'covers': [e[0] for e in ability if e[1] > 1],
               'holes': [e[0] for e in ability if e[1] < 1]}
        
        if output in out.keys():
            return out[output]
        else:
            return ability
    
    def __repr__(self):
        return '{}, Gen {}'.format(self.name, self.gen)
    
    def __str__(self):
        return '{}, a {}/{} gen {} pokemon'.format(self.name.capitalize(), self.ptype, self.stype, self.gen)