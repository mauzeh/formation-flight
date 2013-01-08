import config
from lib.util import tsv_get_column_index
import os

import numpy as np
import matplotlib.pyplot as plt

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

def run():
    
    data_file = '%s/latest.tsv' % config.sink_dir
    
    data = np.loadtxt(
        open(data_file, 'rb'),
        delimiter = "\t",
        skiprows = 1
    )
    
    x = data[:, tsv_get_column_index(data_file, 'config_count_hubs')]
    y = data[:, tsv_get_column_index(data_file, 'avg_formation_size')]
    
    plt.plot(x, y)
    plt.show()