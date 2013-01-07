from .. import run
from lib import sink
import config
import os
import numpy as np

from lib.geo.point import Point

config.lock_time = 60
config.sink_dir = '%s/sink' % os.path.dirname(__file__)

config.hubs = []
for lat in lats:
    for lon in lons:
        config.hubs.append(Point(lat, lon))

def execute():
    run.execute()