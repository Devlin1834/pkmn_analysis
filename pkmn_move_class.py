# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 07:04:53 2019

@author: Devlin
"""

import csv
import numpy as np
import pkmn_types as pet

###############################################################################
## GENERAL VARS & FUNCS #######################################################
###############################################################################
damage_class_name = ['', 'Status', 'Physical', 'Special']
roles = ['P-SWEEP', 'P-TANK', 'P-WALL', 'S-SWEEP', 'S-TANK', 'S-WALL']

###############################################################################
def emptyconvert(x, r, c):
    """ If x is blank, this fucntion will fill it with a value. If it's not
    blank, it will convert it to a compatible value. The values returned are 
    based on arguments passed to the function"""
    
    try:
        y = int(x)
    except ValueError:
        y = 0
    
    nest = {True: {'bool': False,
                   'int': r,
                   'str': r},
            False: {'bool': True,
                    'int': y,
                    'str': x}}
    
    return nest[x == ''][c]

###############################################################################\      /\
## THE MOVE CLASS ##############################################################>----<@]|=
###############################################################################/      \/
class Move():
    def __init__(self, m_id, name, gen, move_type_id, power, pp, accuracy, priority, 
                 damage_class_id, is_z, signature, f_id, f_chance, cat_id, cat, 
                 ail_id, ail, min_h, max_h, min_t, max_t, drain, heal, crit, 
                 ac, fc, sc, kw, sd, samt, stgt):
        
        ## IDs ################################################################
        self.move_id = m_id
        self.move_type_id = int(move_type_id) - 1  
        self.effect_id = f_id
        self.category_id = cat_id
        self.ailment_id = ail_id
        
        ## ID Correspondants ##################################################
        self.name = name
        self.move_type = pet.all_types[self.move_type_id]
        self.damage_class = damage_class_name[int(damage_class_id)] 
        self.category = cat
        self.ailment = ail
        
        ## Basic Data #########################################################         
        self.gen = gen                            
        self.priority = int(priority)             
        self.pp = int(pp)
        self.power = emptyconvert(power, 0, 'int')        
        self.accuracy = emptyconvert(accuracy, 100, 'int') / 100
        
        ## Non-damage Effects #################################################
        self.effect_chance = emptyconvert(f_chance, 100, 'int') / 100
        self.ailment_chance = int(ac)
        self.flinch_chance = int(fc)
        self.stat_chance = int(sc)
        
        ## Stat Changes #######################################################
        self.stats_changed = sd.replace('ALL; ', '').split('; ')
        self.stats_delta = [emptyconvert(i, 0, 'int') for i in samt.split('; ')]
        self.stat_delta_target = emptyconvert(stgt, '', 'int')
        
        ## Additional Data ####################################################
        self.hits = (int(min_h), int(max_h))
        self.turns = (int(min_t), int(max_t))
        self.drain = int(drain)
        self.heal = int(heal)
        self.crit_boost = int(crit)
        
        ## Bools and Keywords #################################################
        self.is_z = emptyconvert(is_z, 0, 'bool')
        self.signature = emptyconvert(signature, 0, 'bool')
        self.keywords = kw.split('; ')
        self.waste = 1 - (.5 * ('charge' in self.keywords or 'recharge' in self.keywords))
        
        ## Derived Data #######################################################
        self.average_damage = sum([self.power * (.8 ** i) for i in range(max(self.hits))]) 
        self.specialized_score = {}
        self.overall_score = 0
        
        ## Fixing Holes in the Data ###########################################
        if '' not in self.stats_changed and self.stat_chance == 0:
            self.stat_chance = 100
            
        if self.ailment_id != '0' and self.ailment_chance == 0:
            self.ailment_chance = 100
    
    ###########################################################################
    def status(self):
        return self.damage_class == 'Status'

    ###########################################################################    
    def energy(self, check):
        return check == self.move_type.name
    
    ###########################################################################
    def set_overall_score(self):
        if len(self.specialized_score) > 0:
            self.overall_score = np.mean(list(self.specialized_score.values()))
        else:
            self.overall_score = 0
        
    ###########################################################################    
    def __repr__(self):
        return '{} {}'.format(self.name, self.move_type.name)
        
    def __str__(self):
        z = {True: 'Z-',
             False: ''}
        
        return '{}: a {} {} type {}move'.format(self.name, self.damage_class, self.move_type.name, z[self.is_z])

###############################################################################
## MOVE CREATION ##############################################################
###############################################################################
moves_refference = list(csv.reader(open("...\\moves_heavy.csv")))
moves_reduced = [move for move in moves_refference]
for move in moves_reduced:
    mname = move[1].replace('-', ' ')
    capped_name = [word.capitalize() for word in mname.split()]
    move[1] = ' '.join(capped_name)
all_moves = [Move(*i) for i in moves_reduced] # 782 Moves in this list

sheer_force = ['Air Slash', 'Ancient Power', 'Astonish', 'Bite', 'Blizzard', 'Body Slam', 'Bubble', 
               'Bubble Beam', 'Bulldoze', 'Charge Beam', 'Confusion', 'Crunch', 'Crush Claw', 
               'Dark Pulse', 'Dragon Rush', 'Dragon Breath', 'Dynamic Punch', 'Earth Power', 
               'Ember', 'Extrasensory', 'Fake Out', 'Fire Blast', 'Fire Fang', 'Fire Punch', 
               'Flame Charge', 'Flame Wheel', 'Flamethrower', 'Flare Blitz', 'Flash Cannon', 
               'Focus Blast', 'Force Palm', 'Gunk Shot', 'Headbutt', 'Heat Wave', 'Ice Beam', 
               'Ice Fang', 'Ice Punch', 'Icy Wind', 'Iron Head', 'Iron Tail', 'Lava Plume', 
               'Liquidation', 'Low Sweep', 'Metal Claw', 'Mud Bomb', 'Mud Shot', 'Mud Shot', 
               'Play Rough', 'Poison Fang', 'Poison Jab', 'Poison Sting', 'Poison Tail', 
               'Power Up Punch', 'Psychic', 'Rock Climb', 'Rock Slide', 'Rock Smash', 'Rock Tomb', 
               'Scald', 'Secret Power', 'Shadow Ball', 'Signal Beam', 'Sky Attack', 'Sludge Bomb',
               'Sludge Wave', 'Snarl', 'Snore', 'Steel Wing', 'Stomp', 'Struggle Bug', 
               'Throat Chop', 'Thunder', 'Thunder Fang', 'Thunderbolt', 'Thunder Punch', 
               'Twister', 'Water Pulse', 'Waterfall', 'Zap Cannon', 'Zen Headbutt']
for move in all_moves:
    if move.name in sheer_force:
        move.keywords.append('Sheer Force')

celebrate = pet.selectro(all_moves, 'celebrate')