# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 13:52:44 2020

@author: Devlin
"""
import sqlite3 as sql
from collections import Counter
###############################################################################
## GENERAL VARIABLES ##########################################################
###############################################################################
type_list = ["Normal", "Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", 
             "Ghost", "Steel", "Fire", "Water", "Grass", "Electric", "Psychic", 
             "Ice", "Dragon", "Dark", "Fairy"]

base_stats = ['HP', 'ATK', 'DEF', 'SPATK', 'SPDEF', 'SPEED']
tank = ['HP', 'DEF', 'SPDEF']

role_map = {'P-SWEEP': [1, 5],       #ATK,    SPD
            'P-WALL':  [0, 2],       #HP,     DEF
            'P-TANK':  [1, 'tank'],  #ATK,    Tank Eval -> max(HP, DEF, SP DEF)
            'S-SWEEP': [3, 5],       #SP ATK, SPD
            'S-WALL':  [0, 4],       #HP,     SP DEF
            'S-TANK':  [3, 'tank']}  #SP ATK, Tank Eval -> max(HP, DEF, SP DEF)

nature_boosts = {'Quirky':  [1, 1, 1, 1, 1, 1],     # Neutral
                 'Adamant': [1, 1.1, 1, .9, 1, 1],  # +Attack,      -Sp. Attack
                 'Jolly':   [1, 1, 1, .9, 1, 1.1],  # +Speed,       -Sp.Attack  
                 'Timid':   [1, .9, 1, 1, 1, 1.1],  # +Speed,       -Attack
                 'Bold':    [1, .9, 1.1, 1, 1, 1],  # +Defense,     -Attack
                 'Impish':  [1, 1, 1.1, .9, 1, 1],  # +Defense,     -Sp. Attack
                 'Modest':  [1, .9, 1, 1.1, 1, 1],  # +Sp. Attack,  -Attack
                 'Calm':    [1, .9, 1, 1, 1.1, 1],  # +Sp. Defense, -Attack
                 'Careful': [1, 1, 1, .9, 1.1, 1]}  # +Sp. Defense, -Sp. Attack

damage_class_name = ['', 'Status', 'Physical', 'Special']
roles = ['P-SWEEP', 'P-TANK', 'P-WALL', 'S-SWEEP', 'S-TANK', 'S-WALL']

###############################################################################
## GENERAL FUNTIONS ###########################################################
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

###############################################################################
###############################################################################
def CAP_convert(CAPBOOL):
    '''converts excel booleans to python booleans'''
    if CAPBOOL == 'TRUE':
        return True
    else:
        return False
 
###############################################################################
###############################################################################
def append_check(growing, array):
    '''appends the first element of an array if the array is populated'''
    if len(array) > 0:
        x = array.pop(0)
        growing.append(x)
        return True
    else:
        return False

###############################################################################
###############################################################################    
def vmod(a, n):
    '''allows me to add negatives without dropping below zero'''
    return max(0, a + n)

###############################################################################
###############################################################################
def pull(array, n):
    '''pulls a stat from an array based on it's name - 
    for use with base stats, calculated stats, evs, ivs, nature boosts'''
    i = base_stats.index(n)
    return array[i]

###############################################################################
###############################################################################
def elise(noun):
    '''inserts a/an based on the following word'''
    x = noun[0].lower()
    vowels = ['a', 'e', 'i', 'o', 'u']
    n = {True: 'n', False: ''}
    
    return 'a{} {}'.format(n[x in vowels], noun)

###############################################################################
###############################################################################
def extract(text):
    '''used to navigate ability keywords - type and numeric effects contained 
    within flower brackets, this func pulls those effects'''
    start = text.find('{') + 1
    end = text.find('}')
    
    return text[start:end]  

###############################################################################
###############################################################################    
def flat_count(lol):
    '''used when analyzing lists of lists. useful for when each pokemon has a
    list of data and we start with a list of pokemon'''
    flat = [t for l in lol for t in l]
    counted = Counter(flat)
    ordered = sorted(counted.items(), key = lambda x: x[1], reverse = True)
    
    return ordered

###############################################################################
###############################################################################
def create_props(lot):
    '''for a list of tuples, creates a list of proportions based on the second
    value. Created for typing analysis where we have [('Fire', 3), ('Water', 4)...]'''
    data = [i[1] for i in lot]
    total = sum(data)
    
    return [round(i / total, 3) for i in data]

###############################################################################
###############################################################################
def paired_print(names, data, char = '-', alt = ' ', m = 1, comment = False):
    '''a simpler way to print organized data. Tablegen3 would be too bulky for
    what this was created for, this prints a slimmer readout of paired data
    char and alt allow us to change the guideline characters
    m is primarily used to move from decimal to percent
    comment is so I can copy/paste from the terminal to the source code'''
    if comment:
        p = '#'
        print('#'*20)
    else:
        p = ''
    
    tippy = max(max([len(i) for i in names]) + 2, 12)
    for i in range(len(names)):
        n = tippy - len(names[i])
        if i % 2 == 1:
            bars = char * n
        else:
            bars = alt *n
            
        print('{}  {} {} {}  {}'.format(p, names[i], bars, data[i] * m, p))
        
    if comment:
        print('#'*20)

###############################################################################
###############################################################################              
def t_order(names, data):
    '''reorders data based on energy types in the order they are written in 
    type_list above'''
    x = [''] * 18
    for i in range(18):
        new_dex = type_list.index(names[i])
        x[new_dex] = data[i]
        
    return x

###############################################################################
###############################################################################           
def SQL_pull(SELECT, FROM, WHERE = False):
    """Pull data from an SQLite table"""
    if WHERE != False:
        w = ' WHERE {}'.format(WHERE)
    else:
        w = ''
        
    conn = sql.connect('POKEMON.db')
    click = conn.cursor()    
    code = "SELECT {} FROM {}{}".format(SELECT, FROM, w)
    click.execute(code)
    data = click.fetchall()
    conn.close()
    
    return data

###############################################################################
###############################################################################
def SQL_run(code):
    """Runs any generic SQL code"""
    conn = sql.connect('POKEMON.db')
    click = conn.cursor()
    click.execute(code)
    conn.commit()
    conn.close()
    
###############################################################################
###############################################################################
def splint(s, i = False):
    """Split Int. Splits my ; seperated lists in SQLite tables"""
    x = s.split('; ')
    if i:
        return [int(q) for q in x]
    else:
        return x
    