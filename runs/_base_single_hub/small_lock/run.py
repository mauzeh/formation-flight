from .. import run
from lib import sink
import config
import os
import numpy as np

from lib.geo.point import Point

config.lock_time = 30
config.sink_dir = '%s/sink' % os.path.dirname(__file__)

# Create custom set of hubs
lats = np.mgrid[ 40: 70: 10j]
lons = np.mgrid[-60: 25: 10j]

config.hubs = []
for lat in lats:
    for lon in lons:
        config.hubs.append(Point(lat, lon))

def execute():
    run.execute()