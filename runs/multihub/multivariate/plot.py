import config
from lib.util import tsv_get_column_index
import os
import math
from lib.util import make_sure_path_exists

import numpy as np
import matplotlib.pyplot as plt

config.sink_dir = '%s/sink' % os.path.dirname(__file__)
config.count_hubs = 5

config.axis_x = {
    'name' : r'$Z$',
    'column' : 'config_Z'
}
config.axis_y = {
    'name' : r'$L$',
    'column' : 'config_lock_time'
}

config.interesting_z_axes = [{
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
    
    axis_x = config.axis_x
    axis_y = config.axis_y
    
    for axis_z in config.interesting_z_axes:
        
        plt.figure()
    
        x = data[:, tsv_get_column_index(data_file, axis_x['column'])]
        y = data[:, tsv_get_column_index(data_file, axis_y['column'])]
        z = data[:, tsv_get_column_index(data_file, axis_z['column'])]
        
        try:
            nx = config.output_nx
            ny = config.output_ny
        except AttributeError:
            N = len(z)
            nx = math.sqrt(N)
            ny = nx

        x = x.reshape(nx, ny)
        y = y.reshape(nx, ny)
        z = z.reshape(nx, ny)
        
        plt.xlabel(axis_x['name'])
        plt.ylabel(axis_y['name'])
    
        plt.contourf(x, y, z, 20)
        plt.colorbar()
        
        #plt.title(r'%s ($n=%d$)' % (axis_z['name'], config.count_hubs))
        plt.title(r'%s' % axis_z['name'])
        
        fig_path = '%s/plot_%s.pdf' % (config.sink_dir, axis_z['column'])
        fig_path = fig_path.replace('/runs/', '/plots/')
        fig_path = fig_path.replace('/sink/', '/')
        make_sure_path_exists(os.path.dirname(fig_path))
        plt.savefig(fig_path)