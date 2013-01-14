import config
from lib.util import tsv_get_column_index
from lib.util import make_sure_path_exists
import os

import numpy as np
import matplotlib.pyplot as plt

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

config.interesting_y_axes = [{
    'name' : 'Distance Penalty',
    'column' : 'distance_penalty'
},{
    'name' : 'Distance Success Rate',
    'column' : 'distance_success_rate'
},{
    'name' : 'Formation Success Rate',
    'column' : 'formation_success_rate'
},{
    'name' : 'Average Formation Size',
    'column' : 'avg_formation_size'
},{
    'name' : 'Fuel Saved',
    'column' : 'fuel_saved'
},{
    'name' : 'Fuel Saved (Without Delay Costs)',
    'column' : 'fuel_saved_disregard_delay'
},{
    'name' : 'Fuel Delay',
    'column' : 'fuel_delay'
}]

def run():
    
    data_file = '%s/latest.tsv' % config.sink_dir
    
    data = np.loadtxt(
        open(data_file, 'rb'),
        delimiter = "\t",
        skiprows = 1
    )
    
    for axis_y in config.interesting_y_axes:
    
        x = data[:, tsv_get_column_index(data_file, 'config_Z')]
        y = data[:, tsv_get_column_index(data_file, axis_y['column'])]
        
        plt.figure()
        
        plt.plot(x, y)
        plt.title(axis_y['name'])
        plt.xlabel(r'Hub Location $Z$')
        plt.ylabel(axis_y['name'])
        plt.grid(True)
        #plt.show()
        
        fig_path = '%s/plot_%s.pdf' % (config.sink_dir, axis_y['column'])
        fig_path = fig_path.replace('/runs/', '/plots/')
        fig_path = fig_path.replace('/sink/', '/')
        make_sure_path_exists(os.path.dirname(fig_path))
        plt.savefig(fig_path)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        