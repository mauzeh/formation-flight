from ..benchmark import run
from lib import sink
import config
import os
import numpy as np
import math

from lib.geo.point import Point

def get_matrix_dimensions():
    
    nx = 25
    ny = 25
    
    return (nx, ny,)

def execute():
    
    config.count_hubs = 3
    config.sink_dir = '%s/sink' % os.path.dirname(__file__)    

    nx, ny = get_matrix_dimensions()
    x_range = np.linspace(0, 1, nx)
    y_range = np.linspace(1, 60, ny)
    run.init()
    
    for x in x_range:

        config.Z = x
    
        for y in y_range:

            config.lock_time = y
            run.single_run()

def plot():

    from ..multivariate import plot as plt
    config.sink_dir = '%s/sink' % os.path.dirname(__file__)
    
    config.axis_x = {
        'name' : r'$L$',
        'column' : 'config_lock_time'
    }
    config.axis_y = {
        'name' : r'$Z$',
        'column' : 'config_Z'
    }
    
    config.output_nx, config.output_ny = get_matrix_dimensions()
    
    plt.run()