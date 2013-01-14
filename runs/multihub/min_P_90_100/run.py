from ..benchmark import run
from lib import sink
import config
import os
import numpy as np

from lib.geo.point import Point

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

def execute():
    
    run.init()
    
    for i in np.linspace(0.9, 1, 10):

        config.min_P = i
        run.single_run()