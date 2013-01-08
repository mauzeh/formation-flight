from ..benchmark import run
from lib import sink
import config
import os
import numpy as np

from lib.geo.point import Point

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

def execute():
    
    run.init()
    
    for slack in np.arange(0, 15, 1):

        config.etah_slack = slack
        run.single_run()