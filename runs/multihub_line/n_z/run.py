from .. import run
from lib import sink
import config
import os
import numpy as np
import math

from lib.geo.point import Point

config.sink_dir = '%s/sink' % os.path.dirname(__file__)
config.legend = r'$H=%d$'

def get_matrix():
    
    x = np.array([1,2,3,6])
    y = np.linspace(0, 1, 100)

    return x,y

def execute():

    run.init()
    x, y = get_matrix()

    for count_hubs in x:

        config.count_hubs = count_hubs
    
        for value in y:

            config.Z = value
            run.single_run()

def plot():

    from .. import plot as plt
    
    config.axis_x = {
        'name' : r'Relative Hub Location $Z$',
        'column' : 'config_Z'
    }
    
    config.x, config.y = get_matrix()
    
    plt.run()