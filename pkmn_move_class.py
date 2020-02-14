# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 07:04:53 2019

@author: Devlin
"""

import numpy as np
import pkmn_toolkit as kit
import pkmn_types as pet
###############################################################################\      /\
## THE MOVE CLASS ##############################################################>----<@]|=
###############################################################################/      \/
class Move():
    def __init__(self, m_id, move_type_id, f_id, cat_id, ail_id, name, damage_class,
                 cat, ail, gen, priority, pp, power, accuracy, f_chance, ac, 
                 fc, sc, sd, samt, stgt, hits, turns, drain, heal, crit,
                 is_z, signature, kw, waste, average_dam, spec_raw):
        
        
        ## IDs ################################################################
        self.move_id = m_id
        self.move_type_id = move_type_id
        self.effect_id = f_id
        self.category_id = cat_id
        self.ailment_id = ail_id
        
        ## ID Correspondants ##################################################
        self.name = name
        self.move_type = pet.all_types[self.move_type_id]
        self.damage_class = damage_class
        self.category = cat
        self.ailment = ail
        
        ## Basic Data #########################################################         
        self.gen = gen                            
        self.priority = int(priority)             
        self.pp = int(pp)
        self.power = int(power)    
        self.accuracy = float(accuracy)
        
        ## Non-damage Effects #################################################
        self.effect_chance = float(f_chance)
        self.ailment_chance = int(ac)
        self.flinch_chance = int(fc)
        self.stat_chance = int(sc)
        
        ## Stat Changes #######################################################
        self.stats_changed = kit.splint(sd)
        self.stats_delta = kit.splint(samt, True)
        self.stat_delta_target = kit.emptyconvert(stgt, 0, 'int')
        
        ## Additional Data ####################################################
        self.hits = kit.splint(hits, True)
        self.turns = kit.splint(turns, True)
        self.drain = int(drain)
        self.heal = int(heal)
        self.crit_boost = int(crit)
        
        ## Bools and Keywords #################################################
        self.is_z = is_z
        self.signature = signature
        self.keywords = kit.splint(kw)
        self.waste = bool(float(waste))
        
        ## Derived Data #######################################################
        self.average_damage = average_dam
        self.spec_raw = kit.splint(spec_raw)
        self.specialized_score = self.read_spec()
        self.overall_score = self.set_overall_score()
        
    
    ###########################################################################
    def status(self):
        '''a quick check if the move is a status move'''
        return self.damage_class == 'Status'

    ###########################################################################    
    def energy(self, check):
        '''a quick check to see what type the move is'''
        return check == self.move_type.name
    
    ###########################################################################
    def set_overall_score(self):
        '''averages all the specialized scores on the move'''
        if len(self.specialized_score) > 0:
            return np.mean(list(self.specialized_score.values()))
        else:
            return 0
    
    ###########################################################################
    def concatenate(self):
        '''writes the specialized scores in a way that can be easily saved
        and read from a sqlie db or a json file'''
        s = ['{}-{}'.format(m, i) for m, i in self.specialized_score.items()]
        return '; '.join(s)
    
    ###########################################################################
    def read_spec(self):
        '''reads the specialized scored when saved with concatenate above'''
        a = {}
        for l in self.spec_raw:
            s = l.split('> ')
            if len(s) == 2:
                name = s[0]
                score = int(s[1])
                a[name] = score
        
        return a
            
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
c_pull = kit.SQL_pull('*', 'moves', 'name = "Celebrate"')[0]
celebrate = Move(*c_pull)