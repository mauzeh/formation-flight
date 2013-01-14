from ..benchmark import run
from lib import sink
import config
import os
import numpy as np
import math

from lib.geo.point import Point

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

def get_matrix_dimensions():
    
    hub_count       = 10
    data_resolution = 5
    
    return (hub_count, data_resolution,)

def execute():
    
    nx, ny = get_matrix_dimensions()
    hub_range = np.linspace(1, nx, nx)
    run.init()

    for count_hubs in hub_range:

        config.count_hubs = count_hubs
    
        for dt in np.linspace(0, 450, ny):

            config.dt = dt
            run.single_run()