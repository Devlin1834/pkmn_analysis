# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 14:18:53 2020

@author: Devlin
"""
from collections import Counter
import random as rn
import pkmn_strategy as sgy
import pkmn_toolkit as kit

name = 'steelix'
monster_set = kit.SQL_pull('*', 'pokemon', 'name = "{}"'.format(name))[0]
mon = sgy.Pokemon(*monster_set)
mon_strats = kit.SQL_pull('*', 'strategies', 'pkmn_id = "{}"'.format(mon.pkmn_id))
target = rn.choice(mon_strats)
strat = sgy.Strategy(*target)


names = kit.SQL_pull('pkmn_id', 'strategies')
flat = [i for l in names for i in l]
c = Counter(flat)
top = kit.SQL_pull('name', 'pokemon', 'pkmn_id = "748"')
print(top) # <- Kommo-o
