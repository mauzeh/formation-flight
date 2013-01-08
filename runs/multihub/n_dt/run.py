from ..benchmark import run
from lib import sink
import config
import os
import numpy as np
import math

from lib.geo.point import Point

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

def execute():
    
    run.init()
    
    for count_hubs in np.arange(1, 20, 1):
        
        config.count_hubs = count_hubs
    
        for dt in np.arange(0, 451, 10):
    
            config.dt = dt
            run.single_run()