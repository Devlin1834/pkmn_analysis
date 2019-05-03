# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 06:30:59 2019

@author: Devlin
"""

import csv
from collections import Counter
import pokemon
import pokemon_offense

refference = list(csv.reader(open("C:\\Users\\Devlin\\Documents\\pokemon.csv")))
species = [i[0].lower() for i in refference]
viable_mons = [x for x in refference if x[10] == 'FALSE' and x[11] == 'TRUE']

all_types = [[i[1].lower(), i[2].lower()] for i in refference]
all_types2 = [sorted(i) for i in all_types]
joined_types = [' '.join(i) for i in all_types2]
types_counted = Counter(joined_types)
types_cns = sorted(list(types_counted.items()), key = lambda x: x[1])
for i in types_cns:
    if i[0][0] == ' ':
        print(i[0][1:] + ": " + str(i[1]))
    else:
        print(i[0] + ": " + str(i[1])) 

print('\nUnique Type Combos\n')    
z = 1
for i in types_cns:
    if i[1] == 1:
        print(str(z) + ' - ' + i[0])
        z += 1
    
print('\nUnused Type Combos\n')

x = 1 
unused = []
for i in pokemon.t:
    for l in pokemon.t:
        if l == i:
            pass
        elif (i + ' ' + l) in types_counted.keys():
            pass
        elif (l + ' ' + i) in types_counted.keys():
            pass
        elif (i.capitalize() + ' ' + l.capitalize()) in unused:
            pass
        else:
            new_type = l.capitalize() + ' '  + i.capitalize()
            print(str(x) + ' - ' + new_type)
            x += 1
            unused.append(new_type)
            
for i in unused:
    print('\n-- ' + i + ' --')
    score_d = sum([x[1] for x in pokemon.deffense_calculator(i.split()[0], i.split()[1])])
    score_o = sum([y[1] for y in pokemon_offense.offense_calculator(i.split()[0], i.split()[1])])
    print('Defensive Score: ' + str(score_d))
    print('Offensive Score: ' + str(score_o))


            
            
            

    