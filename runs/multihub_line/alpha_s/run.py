from .. import run
from lib import sink
import config
import os
import numpy as np
import math

from lib.geo.point import Point

config.sink_dir = '%s/sink' % os.path.dirname(__file__)
config.legend = r'$\alpha=%.2f$'

def get_matrix():
    
    x = np.array([.25, .5, .75, .9])
    y = np.linspace(0, 60, 100)
    
    return x,y

def execute():

    run.init()
    x, y = get_matrix()

    for count_hubs in x:

        config.alpha = count_hubs
    
        for value in y:

            config.etah_slack = value
            run.single_run()

def plot():

    from .. import plot as plt
    
    config.axis_x = {
        'name' : r'Slack $s$',
        'column' : 'config_etah_slack'
    }
    
    config.x, config.y = get_matrix()
    
    plt.run()