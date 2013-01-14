import config
from lib.util import tsv_get_column_index
import os

import numpy as np
import matplotlib.pyplot as plt

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

def run():
    
    run_table()
    run_graph()
    
def run_table():
    
    data_file = '%s/latest.tsv' % config.sink_dir
    
    data = np.loadtxt(
        open(data_file, 'rb'),
        delimiter = "\t",
        usecols = (4,)
    )
    
    x = np.arange(0, 1, .1)
    y = []
    
    for criterium in x:
        count = 0
        for value in data:
            if value >= criterium:
                count += 1
        y.append(count)
        
        print r' %.1f & %d \\' % (
            criterium,
            count
        )

def run_graph():
    
    data_file = '%s/latest.tsv' % config.sink_dir
    
    data = np.loadtxt(
        open(data_file, 'rb'),
        delimiter = "\t",
        usecols = (4,)
    )
    
    x = np.arange(0.01, 1, .01)
    y = []
    
    for criterium in x:
        count = 0
        for value in data:
            if value >= criterium:
                count += 1
        y.append(count)
    
    plt.title(r'Calibration results')
    plt.ylabel(r'Number of aircraft where $P_f\geq P_{f,min}$')
    plt.xlabel(r'Criterium $P_{f,min}$')
    plt.plot(x, y)
    plt.show()
    
