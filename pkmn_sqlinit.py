# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 19:45:54 2020

@author: Devlin                        
"""                
########################################\_____________________________________/
import sqlite3 as sql                ###/                                     \ 
import pkmn_move_class as pmc        ###\_____________________________________/
import pkmn_strategy as sgy          ###/                                     \
import team_calculator5 as tc        ###\_____________________________________/
###############################################################################
## This script adapts my existing data structure to create a SQLite database. 
## After this is successfully run, I should never need to use it again and will
## change my existing data structure. PKMN will never need to update a table, 
## only read it so, this shoudn't be an issue. But it may be confusing if I try
## to read this in the future.
##
##              OLD STRUCTURE --> SQLite DB --> NEW STRUCTURE
##                          inputs      read by
## 
###############################################################################
## GENERAL FUNCS ##############################################################
###############################################################################
def create_connection(db_file):
    """Creates a new database file"""
    conn = None
    try:
        conn = sql.connect(db_file)
        print(sql.version_info)
    except sql.Error as e:
        print('----Connector----')
        print(e)
    finally:
        if conn:
            conn.close()

###############################################################################
###############################################################################           
def open_connection(db_file):
    """Opens a connection to a pre-established databse"""
    conn = None
    try:
        conn = sql.connect(db_file)
        return conn
    except sql.Error as e:
        print('----Opener----')
        print(e)
        
    return conn

###############################################################################
###############################################################################
def create_table(conn, layout):
    """creates a table in a database"""
    try:
        c = conn.cursor()
        c.execute(layout)
    except sql.Error as e:
        print('----Creator----')
        print(e)

###############################################################################
###############################################################################     
def create_row(conn, table, code):
    """adds a row to a table in a database"""
    cur = conn.cursor()
    print(table)
    cur.execute(code, table)
    
###############################################################################
###############################################################################
def code_create(obj, goal = 'create'):
    """writes a base code block so I can copy/pase and edit instead of having
    to type in 30+ column names"""
    array = obj.__dict__
    k = list(array.keys())
    i = [array[s] for s in k]
    
    code = []
    if goal == 'create':
        for x in range(len(k)):
            if type(i[x]) == int:
                snippet = "{} integer".format(k[x])
            elif type(i[x]) == bool:
                snippet = "{} boolean".format(k[x])
            else:
                snippet = "{} text".format(k[x])
            
            code.append(snippet)
            
        return ', \n'.join(code)
    
    elif goal == 'insert':
        top = ', '.join(k)
        bottom = ', '.join(['?' for i in range(len(k))])
        
        return top, bottom
    
###############################################################################
###############################################################################
def all_strategies(array):
    """shows progress for strategy creation because it takes forever and I want 
    to be sure its making decent progress"""
    total = len(array)
    done = 0
    final = []
    for pkmn in array:
        x = pkmn.get_strategies()
        for s in x:
            final.append(s)
        
        done += 1
        pct = round(done / total, 3) * 100
        print('\nDONE {}/{}     -     {}%\n'.format(done, total, pct))
        print('|'*50)
    
    return final
    
##################################################################################/
## SQLite CODE ##################################################################/
################################################################################/
table_abilities = """CREATE TABLE IF NOT EXISTS abilities (
                     ability_id text PRIMARY KEY,
                     name text,
                     role_bonus text,
                     keywords text
                     );"""

insert_ability = """INSERT INTO abilities(ability_id, name, role_bonus, keywords)
                    VALUES(?, ?, ?, ?)"""

table_moves = """CREATE TABLE IF NOT EXISTS moves (
                 move_id integer PRIMARY KEY,
                 move_type_id integer NOT NULL,
                 effect_id text NOT NULL,
                 category_id text,
                 ailment_id text, 
                 name text, 
                 damage_class text, 
                 category text, 
                 ailment text, 
                 gen text, 
                 priority integer, 
                 pp integer, 
                 power integer, 
                 accuracy integer, 
                 effect_chance integer, 
                 ailment_chance integer, 
                 flinch_chance integer, 
                 stat_chance integer, 
                 stats_changed text, 
                 stats_delta text, 
                 stat_delta_target text, 
                 hits text, 
                 turns text, 
                 drain integer, 
                 heal integer, 
                 crit_boost integer, 
                 is_z boolean, 
                 signature boolean, 
                 keywords text, 
                 waste integer, 
                 average_damage integer, 
                 specialized_score text
                 );"""

insert_move = """INSERT INTO moves(move_id, move_type_id, effect_id, category_id, ailment_id, name, damage_class, category, ailment, gen, priority, pp, power, accuracy, effect_chance, ailment_chance, flinch_chance, stat_chance, stats_changed, stats_delta, stat_delta_target, hits, turns, drain, heal, crit_boost, is_z, signature, keywords, waste, average_damage, specialized_score)
                 VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

table_pkmn = """CREATE TABLE IF NOT EXISTS pokemon (
                pkmn_id text PRIMARY KEY, 
                base_id text, 
                name text, 
                ptype_index integer,
                stype_index integer,
                base_hp integer, 
                base_atk integer, 
                base_def integer, 
                base_spatk integer, 
                base_spdef integer, 
                base_spd integer,
                gen text, 
                evolved boolean, 
                legendary boolean, 
                is_mega boolean, 
                can_mega boolean, 
                ability_ids text
                );"""

insert_pkmn = """INSERT INTO pokemon(pkmn_id, base_id, name, ptype_index, stype_index, base_hp, base_atk, base_def, base_spatk, base_spdef, base_spd, gen, evolved, legendary, is_mega, can_mega, ability_ids)
                 VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

table_strats = """CREATE TABLE IF NOT EXISTS strategies (
                  strategy_id integer PRIMARY KEY,
                  name text NOT NULL,
                  pkmn_id integer NOT NULL,
                  mega_id integer,
                  stat_spread text,
                  typing text,
                  ability text,
                  role text,
                  moves text,
                  nature text,
                  ev_spread text,
                  iv_spread text
                  );""" 

insert_strat = """INSERT INTO strategies(name, pkmn_id, mega_id, stat_spread, typing, ability, role, moves, nature, ev_spread, iv_spread)
                  VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

################################################################################\
#################################################################################\
## WORKING CODE ##################################################################\
def database_setup():
    
    #-------------------------------#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # Part 1 >> CREATE THE DATABASE ##>---------------------------------------<>
    #-------------------------------#//////////////////////////////////////////
    
    create_connection('POKEMON.db')
    link = open_connection('POKEMON.db')
    if link is None:
        print('Cannot connect to databse')
        
    all_tables = (table_abilities, table_pkmn, table_strats, table_moves)
    tbls = ('Abilities', 'Pokemon', 'Strategies', 'Moves')
    
    for x in range(4):
        tbl = all_tables[x]
        print('Creating a table for {}'.format(tbls[x]))
        create_table(link, tbl)  
    
    #----------------------------------------------#\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # Part 2 >> RESTRUCTURE DATA TO FIT THE TABLES ##>------------------------<>
    #----------------------------------------------#///////////////////////////
    # Part 2.1 >> SET UP ABILITIES #
    #------------------------------#
    
    sql_abilities = []
    for a in sgy.all_abilities:
        w = a.ability_id
        x = a.name
        y = '; '.join([str(i) for i in a.role_bonus])
        z = '; '.join(a.keywords)
        sql_abilities.append([w, x, y, z])
                            
    #----------------------------#
    # Part 2.2 >> SET UP POKEMON ##>----------------------------------------<##
    #----------------------------#/ Look into Foreign Keys for abilities. I  \#
                                 #\ need an easy way to connect these things /#
                                 ##>----------------------------------------<##
    sql_pkmn = []
    order = ['pkmn_id', 'base_id', 'name', 'ptype_index', 'stype_index', 'base_hp',
             'base_atk', 'base_def', 'base_spatk', 'base_spdef', 'base_spd', 'gen',
             'evolved', 'legendary', 'is_mega', 'can_mega', 'ability_ids']
    
    for p in tc.complete_pkmn:
        array = p.__dict__
        
        sub = []
        for k in order:
            if k == 'ability_ids':
                sub.append('; '.join(p.ability_ids))
            elif k == 'name':
                sub.append(p.name.lower())
            elif k == 'stype_index':
                sec_norms = ('litleo', 'pyroar', 'heliolisk', 'helioptile', 'a-rattata', 'a-raticate')
                if array[k] == 0 and array['name'].lower() not in sec_norms:
                    sub.append(255)
                else:
                    sub.append(array[k])
            else:
                sub.append(array[k])
                
        sql_pkmn.append(sub)
      
    #-------------------------------#
    # Part 2.3 >> SET UP STRATEGIES #
    #-------------------------------# 
    
    all_strats = all_strategies(tc.complete_pkmn)
    sql_strats = []
    
    for s in all_strats:
        a = s.name
        b = s.pkmn_id
        c = s.mega_id
        d = '; '.join([str(i) for i in s.stats_array])
        e = '{}; {}'.format(s.typing.ptype_heavy.type_id, s.typing.stype_heavy.type_id)
        f = s.ability.ability_id
        g = s.role
        h = '; '.join([m.move_id for m in s.moves])
        i = s.nature
        j = '; '.join([str(i) for i in s.ev_spread])
        k = '; '.join([str(i) for i in s.iv_spread])
        sql_strats.append([a, b, c, d, e, f, g, h, i, j, k])
        
    #--------------------------#
    # Part 2.4 >> SET UP MOVES #
    #--------------------------#
    
    sql_moves = []
    order = ['move_id', 'move_type_id', 'effect_id', 'category_id', 'ailment_id', 
             'name', 'damage_class', 'category', 'ailment', 'gen', 'priority', 
             'pp', 'power', 'accuracy', 'effect_chance', 'ailment_chance', 
             'flinch_chance', 'stat_chance', 'stats_changed', 'stats_delta', 
             'stat_delta_target', 'hits', 'turns', 'drain', 'heal', 'crit_boost',
             'is_z', 'signature', 'keywords', 'waste', 'average_damage', 
             'specialized_score']
    
    for m in pmc.all_moves:
        array = m.__dict__
       
        sub = []
        for k in order:
            if k == 'specialized_score':
                sub.append(m.concatenate())
            elif type(array[k]) in (list, tuple):
                o = [str(i) for i in array[k]]
                sub.append('; '.join(o))
            else:
                sub.append(array[k])
        
        sql_moves.append(sub)    
      
    #-----------------------------------#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # Part 3 >> INSERT DATA INTO TABLES ##>-----------------------------------<>
    #-----------------------------------#//////////////////////////////////////
    
    input('PROCEED TO CREATE DB?')
    with link:
        sets = (sql_abilities, sql_pkmn, sql_strats, sql_moves)
        code = (insert_ability, insert_pkmn, insert_strat, insert_move)
        for i in range(4):
            dataset = sets[i]
            run = code[i]
            print('Inserting data on {}'.format(tbls[i]))
            for e in dataset:
                create_row(link, e, run)
         
    link.close()
    
###############################################################################
## IF __NAME__ == "__MAIN__": #################################################
doit = False                  ## Set doit to be True to run the code. This   ##
                              ## prevents me from overwriting the database   ##
                              #################################################

if __name__ =='__main__' and doit:
    database_setup()