#!/usr/bin/env python
"""Simulation bootstrapper"""

from formation_flight.formation import handlers as formation_handlers
from formation_flight.aircraft import handlers as aircraft_handlers
from formation_flight.aircraft import generators
from formation_flight.hub import builders
from formation_flight.hub import allocators
from formation_flight import visualization
from lib.util import make_sure_path_exists

import matplotlib

from lib import sim, debug, sink
from lib.debug import print_line as p

from formation_flight import statistics

from lib.geo.segment import Segment
from lib.geo.route import Route

import config
import os
import numpy as np

from .. import run
from ..europe.run import create_segments

config.count_hubs = 1
config.min_P = 0
config.dt = 0
config.Z = 0.25
config.phi_max = 5
config.etah_slack = 5

config.map_dimensions = {
    'lat' : [ 0., 70.],
    'lon' : [-130., 40.]
}

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

font = {'size' : 20}
matplotlib.rc('font', **font)

def execute():

    planes = run.single_run()
    
    segments = create_segments(planes)

    plt, ax = run.render(segments)

    name = 'count_hubs_%d' % config.count_hubs
    fig_path = '%s/plot_%s.pdf' % (config.sink_dir, name)
    fig_path = fig_path.replace('/runs/', '/plots/')
    fig_path = fig_path.replace('/sink/', '/')

    make_sure_path_exists(os.path.dirname(fig_path))
    
    t = plt.title(r'$H=%d$, $Z=%.2f$, $S_f=%.2f$' % (
        config.count_hubs,
        config.Z,
        statistics.vars['formation_success_rate']
    ))
    t.set_y(1.03)

    plt.show()
