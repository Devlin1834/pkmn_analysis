# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 04:01:09 2019

@author: Devlin
"""
###############################################################################
#@___________________________________________________________________________@#
#|   There are a few problems here, the largest is that it accepts input as  |#
#| columns but we read a cvs by rows. Meaning that it has to be transposed   |#
#| before it can be read into a table. Columns or rows with identical names  |#
#| can't be pulled properly (but thats the users falt, cmon).                |#
#|___________________________________________________________________________|#
###############################################################################
###############################################################################
"""Takes a flat list and converts it to a list of lists, each with len n"""
def list_break(lst, n):
    fin = []
    while len(lst) > 0:
        count = 0
        sub = []
        while count < n:
            x = lst.pop(0)
            sub.append(x)
            count += 1
        fin.append(sub)
        
    return fin

###############################################################################
"""It used to be super readable but I fixed that! Now its _pythonic_ instead.
Designed to be used to transpose data from a csv to make it table-worthy"""
def transpose(lol):  
    return [[s[i] for s in lol] for i in range(len(lol[0]))]
    
###############################################################################
###############################################################################
class Cell():
    def __init__(self, data, col, row, x, y):
        self.data = data
        self.col = col
        self.row = row
        self.x = x
        self.y = y
        
    def __str__(self):
        return '{} in col {} and row {}'.format(self.data, self.col, self.row)
    
    def __repr__(self):
        return self.__str__()

###############################################################################
###############################################################################
class Table():
    def __init__(self, rnames, cnames, data, summary = []):
        self.rnames = [str(i) for i in rnames]
        self.nrows = len(self.rnames)
        
        self.cnames = [str(i) for i in cnames]
        self.ncol = len(self.cnames)
        
        self.raw_data = data
        self.data = self.str_data(self.raw_data)
        
        self.summary = [str(i) for i in summary]
        self.print_summary = len(self.summary) == len(self.cnames)
        
        self.width0 = max((len(n) for n in self.rnames)) + 3
        self.widths = self.get_widths()
        self.border = '-' * (sum(self.widths) + self.width0 + (2 * self.ncol) + 2) 
        self.table = self.generate_table()
    
    ###########################################################################
    def get_cells(self):
        cells = []
        for c in range(self.ncol):
            for r in range(self.nrows):
                cell = Cell(self.raw_data[c][r], self.cnames[c], self.rnames[r], c, r)
                cells.append(cell)
                
        return cells
    
    ###########################################################################
    """Returns a given row or column, based on their names or numbers"""
    def pull(self, given, ask = 'Column'):
        contents = self.get_cells()
        if type(given) is int:
            found = {'Column': [c.data for c in contents if c.x == given],
                    'Row': [c.data for c in contents if c.y == given]}
        else:
            sbjct = given.lower()
            found = {'Column': [c.data for c in contents if c.col.lower() == sbjct],
                    'Row': [c.data for c in contents if c.row.lower() == sbjct]}
            
        return found.get(ask)
    
    ###########################################################################
    """Lets you select the data from a single cell.
    Passing strings lets you select rows and cols by name
    Passing ints lets you select rows and cols by number - starting at 0"""
    def point(self, col, row):
        given = []
        passed = [col, row]
        for v in range(2):
            sbjct = passed[v]
            if type(sbjct) is int:
                ref = [self.cnames, self.rnames][v]
                given.append(ref[sbjct])
            else:
                given.append(sbjct)
 
        x = [p for p in self.get_cells() if [p.col, p.row] == given]
        
        if len(x) > 0:
            sbjct = x[0]
            return sbjct.data
        else:
            return 'Data point does not exist'
        
    ###########################################################################  
    """Sorts a table based on a given column"""
    def col_sort(self, sbjct):
        ## Handle being passed a string
        clow = [i.lower() for i in self.cnames]
        if type(sbjct) is str and sbjct.lower() in clow:
            sbjct = clow.index(sbjct.lower())
        
        ## Step 1: set up the base against which the table will be sorted
        cells = list_break(self.get_cells(), self.nrows)
        base = cells[sbjct]
        source = base.copy()
        base.sort(key = lambda x: str(x.data))
        places = {source.index(x): base.index(x) for x in source}
    
        ## Step 2: compare the other cols to the base and sort accordingly
        second = [lst for lst in cells if lst != base]
        second.insert(0, self.rnames)
        arranged = []
        for lst in second:
            empty = ['' for i in range(len(lst))]
            for pnt in lst:
                dex = lst.index(pnt)
                new = places[dex]
                empty[new] = pnt
            
            arranged.append(empty)
        
        ## Step 3: finalize sorted data
        arranged.insert(sbjct + 1, base)
        self.rnames = arranged.pop(0)
        
        ## Step 4: strip sorted data of the cell class
        reset = []
        for lst in arranged:
            new = [c.data for c in lst]
            reset.append(new)
        
        ## Step 5: re-write attributes based on newly sorted data
        self.raw_data = reset
        self.data = self.str_data(reset)
        
    ###########################################################################
    def row_sort(self, sbjct):
        rlow = [i.lower() for i in self.rnames]
        if type(sbjct) is str and sbjct.lower() in rlow:
            sbjct = rlow.index(sbjct.lower())
            
        cells = list_break(self.get_cells(), self.nrows)
        source = cells.copy()
        cells.sort(key = lambda x: str(x[sbjct].data))
        places = {source.index(x): cells.index(x) for x in source}
        empty = ['' for i in range(self.ncol)]
        for c in range(self.ncol):
            n = self.cnames[c]
            new = places[c]
            empty[new] = n
        
        self.cnames = empty
        
        reset = []
        for lst in cells:
            new = [c.data for c in lst]
            reset.append(new)
         
        self.raw_data = reset
        self.data = self.str_data(reset)
        
    ###########################################################################    
    def str_data(self, lol):
        x = []
        for i in lol:
            x.append([str(o) for o in i])
            
        return x
    
    ###########################################################################    
    def get_widths(self):
        widths = []
        for i in range(len(self.cnames)):
            temp_list = self.data[i].copy() 
            temp_list.append(self.cnames[i])
            if self.print_summary:
                temp_list.append(self.summary[i])
        
            lengths = [len(n) for n in temp_list] 
            widths.append(max(lengths) + 2)
        
        return widths
    
    ###########################################################################    
    def generate_table(self):
        s = " "     # s for space
        b = "|"     # b for bar
        o = "\n|"   # o for opener
        
        table = [self.border]
        
        line = [o + s * self.width0]                               # The blank upper left corner
        for i in self.cnames:
            w = self.cnames.index(i)
            name_box = b + s * (self.widths[w] - len(i)) + i + s
            line.append(name_box)                                  # The Column Names
        table.append("".join(line) + b)
        
        break_line = [o + '-' * self.width0]
        for i in self.widths:
            dash_segment = b + ('-' * (i + 1))                     # The +1 gives an extra dash to cover th column border
            break_line.append(dash_segment)
        table.append("".join(break_line) + b)
        
        for r in range(self.nrows):
            blanks = self.width0 - len(self.rnames[r]) - 1         # The -1 is for the blank space after the row name
            new_line = [o + (s * blanks) + self.rnames[r] + s]
            for c in range(self.ncol):
                point = self.data[c][r]
                blanks = self.widths[c] - len(point)
                column_cell = b + (s * blanks) + point + s
                new_line.append(column_cell)
            
            table.append("".join(new_line) + b)
    
        if self.print_summary:
            table.append("".join(break_line) + b)
            summary = [o + s * self.width0]
            for i in self.summary:
                dex = self.summary.index(i)
                blanks = self.widths[dex] - len(i)
                name_box = b + (s * blanks) + i + s
                summary.append(name_box)
            table.append("".join(summary) + b)
        table.append('\n' + self.border)
            
        return "".join(table)
    
    ###########################################################################
    def __str__(self):
        return self.generate_table()
    
    def __repr__(self):
        return '{} x {} Table Object'.format(self.ncol, self.nrows)
    
###############################################################################
###############################################################################
if __name__ == '__main__':
    a, b, c = ['m', 'n', 'o'], ['a', 'b', 'c'], [[1, 8, 3], [6, '5', 4], ['y', 'x', 'z']]
    # Each sublist in the data set represents a column in the table
    # Table will accept any type of data
    f = Table(a, b, c)
    
    print("Print the entire table\nprint(f)")
    print(f)
    # ---------------------
    # |    |  a |  b |  c |
    # |----|----|----|----|
    # |  m |  1 |  6 |  y |
    # |  n |  8 |  5 |  x |
    # |  o |  3 |  4 |  z |
    # ---------------------
    
    print("\nPull rows and columns by name or number")
    print("f.pull(1, 'Column')  >> {}".format(f.pull(1, 'Column')))
    # f.pull(1, 'Column') >> [6, '5', 4]
    
    print("f.pull('m', 'Row')   >> {}".format(f.pull('m', 'Row')))
    # f.pull('m', 'Row')  >> [1, 6, 'y']
    
    print("\nPull points by names, numbers, or combinations of the two")
    print("f.point(1, 2)      >> {}".format(f.point(1, 2)))
    # f.point(1, 2)     >> 4
    
    print("f.point('a', 'o')  >> {}".format(f.point('a', 'o')))
    # f.point('a', 'o') >> 3
    
    print("f.point(1, 'n')    >> {}".format(f.point(1, 'n')))
    # f.point(1, 'n')   >> 5
    
    print("\nSort the columns lowest to highest\nf.col_sort(1)")
    f.col_sort(1)
    print(f)
    # ---------------------
    # |    |  a |  b |  c |
    # |----|----|----|----|
    # |  o |  3 |  4 |  z |
    # |  n |  8 |  5 |  x |
    # |  m |  1 |  6 |  y |
    # ---------------------
    
    print("\nSort by name or by column index\nf.col_sort('c')")
    f.col_sort('c')
    print(f)
    # ---------------------
    # |    |  a |  b |  c |
    # |----|----|----|----|
    # |  n |  8 |  5 |  x |
    # |  o |  1 |  6 |  y |
    # |  m |  3 |  4 |  z |
    # ---------------------
    
    print("\nSort the rows lowest to highest\nf.row_sort(0)")
    f.row_sort(0)
    print(f)    
    # ---------------------
    # |    |  b |  a |  c |
    # |----|----|----|----|
    # |  n |  5 |  8 |  x |
    # |  m |  6 |  1 |  y |
    # |  o |  4 |  3 |  z |
    # ---------------------
    
    print("\nSort by name or row index\nf.row_sort('o')")
    f.row_sort('o')
    print(f)
    # ---------------------
    # |    |  a |  b |  c |
    # |----|----|----|----|
    # |  n |  8 |  5 |  x |
    # |  m |  1 |  6 |  y |
    # |  o |  3 |  4 |  z |
    # ---------------------