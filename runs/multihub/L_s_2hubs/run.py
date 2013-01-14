from ..benchmark import run
from lib import sink
import config
import os
import numpy as np
import math

from lib.geo.point import Point

config.sink_dir = '%s/sink' % os.path.dirname(__file__)
config.count_hubs = 2
config.runs = 250

def execute():
    
    run.init()
    
    # Output grid is a square
    n = math.sqrt(config.runs)
    
    for lock_time in np.linspace(1, 60, n):
        
        config.lock_time = lock_time
    
        for slack in np.linspace(0, 60, n):
    
            config.etah_slack = slack
            run.single_run()