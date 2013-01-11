from .. import run
from lib import sink
import config
import os
import numpy as np

from lib.geo.point import Point

config.lock_time = 20
config.sink_dir = '%s/sink' % os.path.dirname(__file__)

def execute():
    run.execute()