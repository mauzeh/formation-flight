from ..benchmark import run
from lib import sink
import config
import os
import numpy as np

from lib.geo.point import Point

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

def execute():
    
    run.init()
    
    for Z in np.linspace(0, 1, 25):

        config.Z = Z
        run.single_run()