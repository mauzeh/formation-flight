from ..L_s_1hub import run
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
    
    run.execute()