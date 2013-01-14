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
    
    for count_hubs in np.arange(1, 6, 1):
        
        config.count_hubs = count_hubs
    
        for s in np.arange(0, 60, 3):
    
            config.etah_slack = s
            run.single_run()