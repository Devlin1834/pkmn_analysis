# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 18:09:42 2019

@author: Devlin
"""
def table_gen(row_names, col_names, list_of_lists, summary_row = False):
    """Generates a table for supplied columns. 
    Columns must be supplied as seperate lists
    Everything in the lists need to be strings, it doesn't convert
    There are so many ways to break this function, please be careful
    """   
    rn_lengths = [len(str(n)) for n in row_names]
    widths = [max(rn_lengths)+4]
    for i in range(len(col_names)):
        temp_list = list_of_lists[i].copy()
        temp_list.append(col_names[i])
        if summary_row != False and type(summary_row) == list:
            temp_list.append(summary_row[i])
        lengths = [len(str(n)) for n in temp_list]
        widths.append(max(lengths) + 4)
        
    # The top and bottom of the table
    end_boundary = (sum(widths) + len(col_names) + 2) * '-'
        
    # AND SO IT BEGINS
    print(end_boundary)
    line = ["|" + " "*widths[0]]  # The blank upper left corner
    for i in col_names:
        name_box = "|" + " "*(widths[col_names.index(i)+1] - len(i) - 2) + i + "  "
        line.append(name_box) # The Column Names
    print("".join(line) + "|")
    break_line = []
    for i in widths:
        dash_segment = "|" + '-'*i
        break_line.append(dash_segment)
    print("".join(break_line) + "|")
    row = 0  # Generates one row at a time
    while row < len(row_names):
        for i in range(len(row_names)):
            column = 0 # Each row generates one cell at a time
            new_line = []
            cell = "|" + " "*(widths[0] - len(row_names[i]) - 2) + row_names[i] + "  "
            new_line.append(cell)
            while column < len(col_names):
                column_cell = "|" + " "*(widths[column + 1] - len(list_of_lists[column][i]) - 2) + list_of_lists[column][i] + "  "
                new_line.append(column_cell)
                column += 1
            
            print("".join(new_line) + "|")
            row += 1
    
    if summary_row != False and type(summary_row) == list:
        print("".join(break_line) + "|")
        summary = ["|" + " "*widths[0]]  # The blank lower left corner
        for i in summary_row:
            name_box = "|" + " "*(widths[summary_row.index(i)+1] - len(i) - 2) + i + "  "
            summary.append(name_box) # The Column Summary
        print("".join(summary) + "|")
    print(end_boundary)