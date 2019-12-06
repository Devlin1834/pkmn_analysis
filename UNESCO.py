# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 04:34:35 2018

@author: Devlin
"""

from collections import Counter
import matplotlib.pyplot as plt
import csv

def sorted_hbar_gen(file = None, data = None, title = 'Sorted By Category', xlab = 'Count', ylab = 'Category', output_name = None):
    try:
        if file != None:
            csv_lol = list(csv.reader(open(file)))
            raw = [d[0] for d in csv_lol]
        elif file == None and data == None:
            3/0
        else:
            raw = data
    except ZeroDivisionError:
        print("You have to supply data, moron")
        print("So pick to use a CSV or a pre-loaded data-list")
        print("'file = ' for a CSV or 'data = ' for a pre-loaded data-set")
    else:   
        data = Counter(raw)
        data_tuples = list(data.items())
        data_sorted = sorted(data_tuples, key = lambda x: x[1])   
        data_list = [i[0] for i in data_sorted]
        data_enum = [e for e, i in enumerate(data_list)]
        counts = [i[1] for i in data_sorted]   
        plt.figure(figsize = (8, len(counts)/4.5))
        plt.barh(data_enum, counts)
        plt.ylabel(ylab)
        plt.yticks(data_enum, data_list)
        plt.xlabel(xlab)
        plt.title(title)
        plt.grid()
        plt.show()
    
        if output_name != None:
            try:
                output = open(output_name, 'w', newline = '')
                output_writer = csv.writer(output)
                for t in data_sorted:
                    output_writer.writerow(t)
                output.close()
            except TypeError:
                print("\nCannot write without a designated filename")
                print("Specify 'output_name = ' as an argument")