# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 06:08:23 2019

@author: Devlin
"""

import csv
import numpy as np
import random as rn
import table_gen3 as tg3
import pkmn_types as pet
import pkmn_move_class as pmc

###############################################################################
## SECONDARY CLASSES ##########################################################
###############################################################################
class Ability():
    def __init__(self, a_id, name, ps, pt, pw, ss, st, sw, keywords = 'NA; NA'):
        self.ability_id = a_id
        self.ugly_name = name
        self.role_bonus = [int(ps), int(pt), int(pw), int(ss), int(st), int(sw)]
        self.keywords = keywords.split('; ')
        self.name = self.rename()
    
    ###########################################################################    
    def rename(self):
        aname = self.ugly_name.replace('-', ' ')
        capped_name = [word.capitalize() for word in aname.split()]
        
        return ' '.join(capped_name)
    
    ###########################################################################
    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.name
    
###############################################################################
class Move_Point():    
    def __init__(self, p_id, v_id, m_id, t_id, level, order):
        self.pkmn_id = p_id
        self.pkmn_version_id = v_id     # I use v_id == 18 for USUM
        self.move_id = m_id
        self.method_id = t_id
        self.level = level
        self.order = order

###############################################################################
## GENERAL VARS & FUNCS #######################################################
###############################################################################
def CAP_convert(CAPBOOL):
    if CAPBOOL == 'TRUE':
        return True
    else:
        return False
    
###############################################################################
def append_check(growing, array):
    if len(array) > 0:
        x = array.pop(0)
        growing.append(x)
        return True
    else:
        return False

###############################################################################    
def vmod(a, n):
    return max(0, a + n)

###############################################################################
def pull(array, n):
    i = base_stats.index(n)
    return array[i]

###############################################################################
def elise(noun):
    x = noun[0].lower()
    vowels = ['a', 'e', 'i', 'o', 'u']
    n = {True: 'n', False: ''}
    
    return 'a{} {}'.format(n[x in vowels], noun)

###############################################################################
def extract(text):
    start = text.find('{') + 1
    end = text.find('}')
    
    return text[start:end]            

###############################################################################
base_stats = ['HP', 'ATK', 'DEF', 'SPATK', 'SPDEF', 'SPEED']
tank = ['HP', 'DEF', 'SPDEF']

roles = {'P-SWEEP': [1, 5],          #ATK,    SPD
         'P-WALL':  [0, 2],          #HP,     DEF
         'P-TANK':  [1, 'tank'],     #ATK,    Tank Eval -> max(HP, DEF, SP DEF)
         'S-SWEEP': [3, 5],          #SP ATK, SPD
         'S-WALL':  [0, 4],          #HP,     SP DEF
         'S-TANK':  [3, 'tank']}     #SP ATK, Tank Eval -> max(HP, DEF, SP DEF)

nature_boosts = {'Quirky':  [1, 1, 1, 1, 1, 1],     # Neutral
                 'Adamant': [1, 1.1, 1, .9, 1, 1],  # +Attack,      -Sp. Attack
                 'Jolly':   [1, 1, 1, .9, 1, 1.1],  # +Speed,       -Sp.Attack  
                 'Timid':   [1, .9, 1, 1, 1, 1.1],  # +Speed,       -Attack
                 'Bold':    [1, .9, 1.1, 1, 1, 1],  # +Defense,     -Attack
                 'Impish':  [1, 1, 1.1, .9, 1, 1],  # +Defense,     -Sp. Attack
                 'Modest':  [1, .9, 1, 1.1, 1, 1],  # +Sp. Attack,  -Attack
                 'Calm':    [1, .9, 1, 1, 1.1, 1],  # +Sp. Defense, -Attack
                 'Careful': [1, 1, 1, .9, 1.1, 1]}  # +Sp. Defense, -Sp. Attack

###############################################################################
learnset_raw = list(csv.reader(open("...\\pokemon_learnset.csv")))
workable = [Move_Point(*i) for i in learnset_raw]
mids = [move.move_id for move in pmc.all_moves]

abilities_raw= list(csv.reader(open("...\\abilities.csv")))
all_abilities = [Ability(*i) for i in abilities_raw] # 233 Abilities in this list
aids = [a.ability_id for a in all_abilities]

###############################################################################
## BASE POKEMON CLASS #########################################################
###############################################################################
class Pokemon():
    def __init__(self, p_id, name, ptype, stype, stat_hp, stat_atk, stat_def, stat_spatk, stat_spdef, stat_spd, gen, legendary, evolved, is_mega, can_mega, base_id, a_one, a_two, hidden):
        self.pkmn_id = p_id
        self.base_id = base_id
        
        self.name = name.capitalize()
        self.ptype_index = pet.t.index(ptype)
        self.ptype = pet.all_types[self.ptype_index]
        
        if stype == '':  ######################################################  I have dreams of 
            self.stype_index = False                                          # removing this if-block
            self.stype = False                                                # but as of now, they are
        else:                                                                 # but dreams... sweet 
            self.stype_index = pet.t.index(stype)                             # dreams
            self.stype = pet.all_types[self.stype_index]  #####################
            
        self.base_hp = int(stat_hp)
        self.base_atk = int(stat_atk)
        self.base_def = int(stat_def)
        self.base_spatk = int(stat_spatk)
        self.base_spdef = int(stat_spdef)
        self.base_spd = int(stat_spd)
        self.base_array = [self.base_hp, self.base_atk, self.base_def,
                           self.base_spatk, self.base_spdef, self.base_spd]
        self.bulk = [pull(self.base_array, i) for i in tank]
        self.bst = sum(self.base_array)
        
        self.gen = gen
        self.evolved = CAP_convert(evolved)
        self.legendary = CAP_convert(legendary)
        self.is_mega = CAP_convert(is_mega)
        self.can_mega = CAP_convert(can_mega)
        
        self.ability_ids = [a_one, a_two, hidden]
        self.abilities = [all_abilities[aids.index(i)] for i in self.ability_ids if i != '']
        
        self.build = 0
    
    ###########################################################################
    def get_std(self):
        return round(np.std(self.base_array), 2)
    
    ###########################################################################
    def get_role_array(self):
        role_scores = []
        
        for key in roles:
            sone = roles[key][0] 
            stwo = roles[key][1]
            if type(stwo) is str:
                r_score = self.base_array[sone] + max(self.bulk)
                role_scores.append([key, r_score])
            else:
                r_score = self.base_array[sone] + self.base_array[stwo]
                role_scores.append([key, r_score])
                
        final = sorted(role_scores, key = lambda x: x[1], reverse = True)
        
        return final
               
    ###########################################################################
    def get_strategies(self):
        strats = []
        ident = (self.pkmn_id, self.base_id)
        energy = (self.ptype, self.stype)
        valid = [i for i in self.abilities if 'GIMMICK' not in i.keywords]
        run = {True: valid,
               False: [rn.choice(self.abilities)]}
        
        rscores = self.get_role_array()
        
        for a in run[len(valid) > 0]:
            for r in rscores:
                dex = pmc.roles.index(r[0])
                bonus = a.role_bonus[dex]
                r[1] += bonus
                
            ordered = sorted(rscores, key = lambda x: x[1], reverse = True)        
            viable = [r[0] for r in ordered if r[1] >= 200]
            search = {True: viable,
                      False: [ordered[0][0]]}
            
            for r in search[len(viable) > 0]:
                g = Strategy(self.name, ident, self.base_array, energy, r, a)
                strats.append(g)
                
        lim = .9
        peak = max([s.strategic_score for s in strats])
        return [s for s in strats if s.strategic_score >= lim * peak]                 
        
    ###########################################################################
    def print_statblock(self, view = 255):
        builds = self.get_strategies()
        if view in range(len(builds)):
            sets = [builds[view]]
        else:
            sets = sorted(builds, key = lambda x: x.strategic_score, reverse = True)
        
        for s in sets:
            print('-'*25)
            print("{} runs {} nature".format(s.name, elise(s.nature)))
            for i in range(6):
                empty = len('SPEED') - len(base_stats[i])
                bar = int(s.stats_array[i] / 30)
                if s.ev_spread[i] != 0:
                    e = ' +EV'
                else:
                    e = ''
                
                print("{}{}: {} ({}) {}{}".format(' '*empty, base_stats[i], '|'*bar, self.base_array[i], s.stats_array[i], e))
            
            print('-'*25)
            for m in s.algo_moveset:
                print('{} >> {}'.format(m.specialized_score[s.name], m))
        
    ###########################################################################
    def __repr__(self):
        return '{}, Gen {}'.format(self.name, self.gen)
    
    def __str__(self):
        if not self.stype:
            s = ''
        else:
            s = '/' + str(self.stype.name)
        
        return '{}, {}{} type from gen {}'.format(self.name, 
                elise(self.ptype.name), s, self.gen)
     ##########################################################################################\   
    ###########################################################################################|
   ## So the Pokemon Class contains all the raw data for the pokemon, and    ##################/
  ### its job is to identify ideal strategies the pokemon can run. Then it   #####  
 #### passes those strategies to the strategies class where moves get picked ####
##### and scores get finalized for rankings.                                 ###  
###############################################################################    
##############################################################################
class Strategy():
    def __init__(self, mon, identifiers, stat_spread, types, role, ability):
        self.mon = mon
        self.pkmn_id = identifiers[0]
        self.mega_id = identifiers[1]
        self.base_spread = stat_spread
        self.typing = pet.Typing(*types)
        self.ability = ability
        
        self.role = role
        self.nature = self.nature_select()
        self.ev_spread = self.spread_evs()
        self.iv_spread = [31 for i in range(6)]
        self.stats_array = self.calculate_stats(input_evs = self.ev_spread, input_nature = self.nature)
        self.speed = self.stats_array[5] # Speed gets used a lot, so it gets a special variable
        self.bulk = sum([pull(self.stats_array, i) for i in tank])
        
        self.name = '{} {} {}'.format(self.role, self.ability.name, self.mon)
        
        self.move_list = self.get_moves('names')
        self.moves = self.get_moves('moves')
        self.algo_moveset = self.moveset_algorithm()
        
        self.strategic_score = self.get_score()
    
    ###########################################################################    
    def ability_modify(self):
        for w in self.ability.keywords:
            e = extract(w)
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
                d = base_stats.index(e)
                self.iv_spread[d] = 0
            elif 'HIT' in w:
                o = self.typing.offensive_raw
                g = [i for i in o if i[0] == 'Ghost'][0]
                g[1] = min(g[1], 1)
        
    ###########################################################################
    def running(self, name, check = 'ability'):
        see = {'ability': self.ability.name,
               'nature': self.nature,
               'role': self.role}
        
        return see[check] == name
    
    ###########################################################################
    def get_moves(self, output):
        place = {True: self.pkmn_id,
                 False: self.mega_id}
        
        raw = [move for move in workable if move.pkmn_id == place[self.mega_id == '']]
        indicies = list(set([mids.index(move.move_id) for move in raw]))
        moves = sorted([pmc.all_moves[i] for i in indicies], key = lambda x: x.name)
        
        out = {'names': [move.name for move in moves],
               'moves': moves}
        
        return out[output]
    
    ###########################################################################
    def spread_evs(self):
        stat_focus = roles[self.role]
        if stat_focus[1] == 'tank':
            ss = [[i, pull(self.base_spread, i)] for i in tank]
            ss.sort(key = lambda x: x[1])
            n1 = ss[0][0]
            one = base_stats.index(n1)
        else:
            one = stat_focus[1]
            n1 = base_stats[one]
        
        two = stat_focus[0]
        
        spread = [0 for i in range(6)]
        spread[one] = 252
        spread[two] = 252
        
        return spread
        
    ############################################################################# 
    ####### SCORE MOVES - where the magic happens ###############################
    ## This function is a little intense and I may try to break it up later,   ##
    ## but for now it has to stay, at least until I finish balancing it. In    ## 
    ## case you can't tell, I hate IF trees and try to avoid the at all costs  ##
    ## so ability integration is really killing me. I have tried to keep it    ##
    ## readable and efficient, but have obviously failed in some places.       ## 
    ## I really milk the hell out of booleans so be sure to understand those   ##
    #############################################################################
    def score_moves(self):
        priority_balance = {True:  2000 / self.speed,
                            False: (1000 - self.bulk) / 10}
        
        flinch_balance = {True:  .3,
                          False: .8} 
        
                         ###########################\ 
        ailment_bonus = {35: [1, 4],               #-Paralysis/Burn 
                         30: [2, 3, 5], ############-Poison/Sleep/Frozen
                         25: [21],                 #-Ingrain
                         20: [6, 7, 8, 9, 18], #####-Confusion/Infatuation/Trap/Nightmare/Leech Seed
                         15: [12.14, 17, 20],      #-Torment/Yawn/Foresight/Perish Song
                         10: [25], #################-Grounded
                         5:  [13, 15, 19, 24]}     #-Disable/Heal Block/Embargo/Silence
                         ###########################/
        
                       ###################################################\ 
        gimmick_mod = {'8':    -100,                                     # 008 - Self Destruct/Explosion
                       '9':    -60, ###################################### 009 - Dream Eater
                       '247':  -80,                                      # 247 - Last Resort
                       '28':   -20, ###################################### 028 - Thrash/Petal Dance/Outrage
                       '310':  -30,                                      # 310 - Heal Pulse 
                       '293':  -80, ###################################### 293 - Synchronoise
                       '29':    10,                                      # 029 - Whirlwind/Roar/Dragon Tail/Circle Throw 
                       '143':  -20000 / pull(self.stats_array, 'HP'), #### 143 - Belly Drum
                       '400':  -20}                                      # 400 - Purify
                       ###################################################/
        
        ability_tc = {'Refridgerate': 'Ice',
                      'Pixilate':     'Fairy',
                      'Galvanize':    'Electric',
                      'Aerielate':    'Flying'}
        
        ps = {'Physical': pull(self.stats_array, 'ATK'),
              'Special':  pull(self.stats_array, 'SPATK'),
              'Status':   0}
        
        scoreable = []
        for m in self.moves:
            if m.category == 'gimmick':
                m.specialized_score[self.name] = 0
            else: 
                scoreable.append(m)
        
        ## SCORING PROCESS ####################################################
        for move in scoreable:
            sheer = self.running('Sheer Force') and 'Sheer Force' in move.keywords
            power = (self.running('Pure Power') or self.running('Huge Power')) and move.damage_class == 'Physical'
        
            no_guard = {True:  1,
                        False: move.accuracy}
            
            atk = ps[move.damage_class] * (1 + power)
            
            technician = (.5 * (self.running('Technician') and move.power <= 60)) + 1
            
            skill_link = {True:  max(move.hits) * move.power,                                           ##############################################
                          False: move.average_damage}                                                   #  Hey, where the hell did .0022 come from?  #
                                                                                                        # Well its based on the damage formula. The  #
            dclass = {True:  50.0,                                                                      # Coefficients work out to...                #
                      False: 00.0022 * skill_link[self.running('Skill Link')] * atk * technician} #######        42/50 * power * (atk / def)         #
                                                                                                        # 42/50 evaluates to .84 and the defense     #
            start = dclass[move.status()]                                                               # of a Bold Arceus with perfct IV/EVs is 367 #
            other = 1                                                                                   #      .84 / 367 = .0022 and change.         #
                                                                                                        ##############################################
            ## CATEGORY #######################################################
            if move.category == 'ailment':
                start = vmod(start, 50 * ('SWEEP' in self.role) - 30)
            elif move.category == 'hazzard' and 'SWEEP' not in self.role:
                start = vmod(start, 20)
            elif move.category == 'unique':
                start = vmod(start, -40)
            
            ## AILMENTS #######################################################    
            for key in ailment_bonus:
                if int(move.ailment_id) in ailment_bonus[key] and not sheer:
                    start = vmod(start, (move.ailment_chance / 100) * key)
            
            ## CRITICAL HITS ##################################################
            multihit = {True: max(move.hits),
                        False: np.mean(move.hits)}
            
            norm = not move.status()
            chance = .0625 * multihit[self.running('Skill Link')] * norm
            
            level = 1 + self.running('Super Luck') + move.crit_boost
            crit = 1 + (chance * (1.5 + (.5 *self.running('Sniper'))) * level)
            other *= crit 
            
            ## UNIQUE MOVES ###################################################################\
            if move.effect_id == '229' and self.speed < 170 and 'TANK' in self.role: ########### Volt Switch and U-Turn
                start = vmod(start, 20)                                                      ##|
            elif move.effect_id == '80': ####################################################### Substitute
                start = vmod(start, (self.bulk - 750) / 4)                                   ##|
            elif move.effect_id == '110' and 'Ghost' in self.typing.types: ##################### Curse
                start = vmod(start, -40)                                                     ##|
            elif move.effect_id == '112' and 'WALL' in self.role: ############################## Protect and Detect 
                start = vmod(start, 10)                                                      ##|
            elif move.effect_id == '252' and 'WALL' in self.role: ############################## Aqua Ring
                start = vmod(start, .0002 * self.bulk * pull(self.stats_array, 'HP'))        ##| 
            elif move.effect_id in ['356', '362'] and 'SWEEP' not in self.role: ################ Kings Shield and Spikey Shield
                start = vmod(start, 30)                                                      ##|
            elif move.effect_id in gimmick_mod.keys(): ######################################### Shit Moves
                start = vmod(start, gimmick_mod[move.effect_id])                             ##| 
                                                                                             ##|
            ## PRIORITY #######################################################################/             
            is_gale = self.running('Gale Wings') and move.energy('Flying')
            is_prank = self.running('Prankster') and move.status()
            is_nurse = self.running('Triage') and move.category == 'heal'
            
            prio = {True: 1,
                    False: move.priority != 0}
            
            stall = {True: -6,
                     False: prio[is_gale or is_prank or is_nurse]}
            
            u = stall[self.running('Stall')]
            p = priority_balance[move.priority > 0]
            s = not move.status() + .5
            start = vmod(start, u * p)
            
            ## FLINCH #########################################################
            flinch_utility = (self.speed > 225 or move.priority > 0) and not sheer
            f = flinch_balance[move.flinch_chance == 100] * flinch_utility * (1 + self.running('Serene Grace'))
            start = vmod(start, move.flinch_chance * f)
            
            ## HEAL DRAIN RECOIL ##############################################
            r = not (move.drain < 0 and ('SWEEP' in self.role or self.running('Rock Head')))
            other *= 1 + (move.drain * .01 * r)
            start = vmod(start, move.heal * (self.bulk / 750) * (.5 + ('SWEEP' not in self.role)))
            
            ## STAB AND COVERAGE ##############################################
            menergy = move.move_type.name  ## SUPPORT THE PATRIARCHY WITH OPPRESSIVE VARIABLE NAMES
            nchange = ability_tc.get(self.ability.name)
            skill_link = self.running('Skill Link') and max(move.hits) > 0
            steelworker = self.running('Steelworker') and move.energy('Steel')
            lvoice = self.running('Liquid Voice') and 'sound' in move.keywords
            protean = self.running('Protean')
            normalize = self.running('Normalize')
            changes = nchange != None and move.energy('Normal')
            stab = self.typing.tcheck(menergy) or steelworker or normalize or changes or lvoice or protean
            
            if stab and not move.status():
                other *= (1.5 + (.5 *self.running('Adaptablility')) + (.2 * changes))
            
            elif self.typing.tcheck(menergy, 'need') and not move.status():
                l = [menergy] + [nchange for i in range(changes)] + ['Water' for i in range(lvoice)]
                c = [i for i in self.typing.get_coverage() if i in l]
                start = vmod(start, (len(c) * 5) + 5)

            ## ABILITIES ######################################################            
            terrors = {'Strong Jaws': 'bite',
                       'Mega Launcher': 'pulse',
                       'Iron Fist': 'punch',
                       'Tough Claws': 'contact'}
            
            boosts = {'Swarm': 'Bug', 
                      'Overgrow': 'Grass', 
                      'Blaze': 'Fire',
                      'Torrent': 'Water'}
            
            simple = {'Parental Bond': 1.5,
                      'Compound Eyes': 1.125}
            
            if self.ability.name in terrors.keys() and terrors[self.ability.name] in move.keywords:
                other *= 1.5 - (.3 * self.running('Tough Claws'))
            elif self.ability.name in simple.keys():
                other *= simple[self.ability.name]
            elif self.running('Analytic') and not move.status() and move.priority <= 0:
                other *= 1 + ((50 / self.speed))
            elif self.running('Poison Touch') and 'contact' in move.keywords:
                start = vmod(start, 6)
            elif self.ability.name in boosts.keys() and move.energy(boosts[self.ability.name]):
                other *= 1.165
            elif sheer:
                other *= 1.3
            
            ## STAT CHANGES ###################################################
            curse_boost = (move.effect_id == '110' and 'Ghost' not in self.typing.types)
            stats_self = ('' not in move.stats_changed and move.stat_delta_target)
            stats_target = ('' not in move.stats_changed and not move.stat_delta_target)
            g = 1 + self.running('Serence Grace')
            a = min(move.stat_chance * g, 60) / 60
            modded_stats = base_stats + ['ACC', 'EVA']
            battle_stats = self.stats_array + [0, 0]
            
            if curse_boost:
                subject = ['ATK', 'DEF', 'SPEED']
                chchchanges = [1, 1, -1]
            else:
                subject = move.stats_changed.copy()
                chchchanges = move.stats_delta.copy()
            
            if stats_target and not sheer:
                for s in range(len(subject)):
                    lower = subject[s]
                    psoften = lower == 'DEF' and self.role in ['P-SWEEP', 'P-TANK']
                    pweaken = lower == 'ATK' and self.role in ['P-TANK', 'P-WALL']
                    ssoften = lower == 'SPDEF' and self.role in ['S-SWEEP', 'S-TANK']
                    sweaken = lower == 'SPATK' and self.role in ['S-TANK', 'S-WALL']
                    b = -10 - (20 * (psoften or pweaken or ssoften or sweaken))              
                    start = vmod(start, a * b * chchchanges[s])                             
                                                                                             #|_____________________________________________________________________|
            elif (stats_self or curse_boost) and not sheer:                                 ##|                                                                     |
                for i in range(len(subject)):                                              ###|             IS                                                      |
                    s = subject[i]                                                        ####|                                                                     |
                    chance_to_hit = {True: 250,                                          #####|                           IT                                        |
                                     False: battle_stats[modded_stats.index(s)]}        ######|                                                         ?           |
                    delta = chchchanges[i] * (2 * (not self.running('Contrary')) - 1)  #######|      ?                                                              |
                    s_value = chance_to_hit[s in ['ACC', 'EVA']]                      ########|                                                REALLY               |                        
                                                                                     #########|                          PROGRAMMING                                |
                    if delta > 0:                                                   ##########|                                                                     | 
                         muy_rapido = {True: 250 / self.speed,                     ###########|              WITHOUT                                                |
                                       False: s_value * .1}                       ############|                                                        ?            |
                                                                                 #############|                                ELABORTE                             |
                         b = muy_rapido[s == 'SPEED']                           ##############|                                                                     |
                         de = move.stat_chance == 100 and not move.status()    ###############|                                        ASCII ART                    |
                         c = 1 - (.5 * de)                                    ################|            ?                                                        |
                         start = vmod(start, delta * a * b * c)              #################|                                                                     |
                                                                                           ###|                     COMMENTS                                        |
                    else:                                                                  ###|                                                    ?                |
                         passed = False                                                    ###|       ?                                                             |
                         if 'ATK' in subject and 'SPATK' in subject and not passed:        ###|                                                                     | 
                             passed = True                                                 ###|                                            ?                        |
                         else:                                                             ###|_____________________________________________________________________|
                             trop_vite = 'SWEEP' in self.role and s in ['DEF', 'SPDEF']    #########################################################################|
                             bonus = self.speed * trop_vite
                             b = 4000 / (s_value + bonus)
                             start = vmod(start, delta * a * b)
                             
            ###################################################################
            acc = no_guard[self.running('No Guard')]
            move.specialized_score[self.name] = int(start * acc * other * move.waste)
                
    ###########################################################################
    def moveset_algorithm(self):
        self.score_moves()
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
            
            added = append_check(moveset, l)
            if not added:
                moveset.append(pmc.celebrate)
                if self.name not in pmc.celebrate.specialized_score.keys():
                    pmc.celebrate.specialized_score[self.name] = 0
                                
        return moveset
    
    ###########################################################################
    def calculate_stats(self, input_ivs = [31]*6, input_evs = [0]*6, input_nature = 'Quirky', level = 100):     
        self.ability_modify()
        IVs = input_ivs.copy()
        EVs = input_evs.copy()
        nature = nature_boosts[input_nature]
        
        HP = (((2 * pull(self.base_spread, 'HP') + IVs[0] + (EVs[0] / 4)) * level) / 100) + level + 10
        stats = [int(HP)]
        for i in range(1, 6):
            s = ((((2 * self.base_spread[i] + IVs[i] + (EVs[i] / 4)) * level) / 100) + 5) * nature[i]
            stats.append(int(s))        
        
        return stats
    
    ###########################################################################
    def nature_select(self):
        stat_focus = roles[self.role]
        if stat_focus[1] == 'tank':
            ss = [[i, pull(self.base_spread, i)] for i in tank if i != 'HP']
            ss.sort(key = lambda x: x[1], reverse = True)
            n1 = ss[0][0]
            one = base_stats.index(n1)
        else:
            one = stat_focus[1]
            n1 = base_stats[one]

        wall_check = {True: one,
                      False: stat_focus[0]}
        
        two = wall_check[stat_focus[0] == 0]
        n2 = base_stats[two]
        
        fs = [[n1, self.base_spread[one]], [n2, self.base_spread[two]]]
        fs.sort(key = lambda x: x[1])
        focus_stat = fs[0][0]
        primary = base_stats.index(focus_stat)
        
        docked_stat = {True: 1,
                       False: 3}
        
        secondary = docked_stat['S-' in self.role]
        
        for key in nature_boosts:
            l = nature_boosts[key]
            if l[primary] == 1.1 and l[secondary] == .9:
                return key
    
    ###########################################################################
    def get_score(self):
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
        
        sone = roles[self.role][0]
        stwo = roles[self.role][1]
        if stwo == 'tank':
            x = max([pull(self.stats_array, i) for i in tank if i != 'HP'])
        else:
            x = self.stats_array[stwo]
            
        y = self.stats_array[sone]
        
        rdex = pmc.roles.index(self.role)
        a = self.ability.role_bonus[rdex]
        
        return role_mods[self.role[2:]] + m + x + y + a
        
    ###########################################################################    
    def print_move_analysis(self):
        x = sorted(self.moves, key = lambda x: x.specialized_score[self.name], reverse = True)
        for move in x:
            print('{} -- {}'.format(move, move.specialized_score[self.name]))
    
    ###########################################################################       
    def print_type_effectiveness(self):
        o = sorted(self.typing.offensive_raw, key = lambda x: x[0])
        d = sorted(self.typing.defensive_raw, key = lambda x: x[0])
        
        n = [i[0] for i in o]
        c = ['Offensive', 'Defensive']
        a = [[i[1] for i in o], [i[1] for i in d]]
        
        etable = tg3.Table(n, c, a)
        print(etable.table)
      
    ###########################################################################
    def __repr__(self):
        return '{}'.format(self.name)
    
    def __str__(self):      
        return '{}: {}'.format(self.name, self.stategic_score)
    
###############################################################################