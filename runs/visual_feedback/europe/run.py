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

import config
import os
import numpy as np

config.count_hubs = 2
config.min_P = 0.12
config.dt = 0
config.Z = 0.1
config.phi_max = 15
config.etah_slack = 30

config.map_dimensions = {
    'lat' : [ 35., 70.],
    'lon' : [-20., 20.]
}

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

font = {'size' : 20}
matplotlib.rc('font', **font)

def execute():
    single_run()

def single_run():
    sim.init()
    aircraft_handlers.init()
    formation_handlers.init()
    statistics.init()
    visualization.init()

    # Construct flight list
    planes = generators.get_via_stdin()

    # Find hubs
    config.hubs = builders.build_hubs(planes, config.count_hubs, config.Z)

    # Allocate hubs to flights
    allocators.allocate(planes, config.hubs)
    
    for flight in planes:
        sim.events.append(sim.Event('aircraft-init', flight, 0))
    
    sim.run()

    name = 'count_hubs_%d' % config.count_hubs

    plt, ax = visualization.render()
    fig_path = '%s/plot_%s.pdf' % (config.sink_dir, name)
    fig_path = fig_path.replace('/runs/', '/plots/')
    fig_path = fig_path.replace('/sink/', '/')
    make_sure_path_exists(os.path.dirname(fig_path))

    plt.title(r'$H=%d$, $Z=%.2f$, $S_f=%.2f$' % (
        config.count_hubs,
        config.Z,
        statistics.vars['formation_success_rate']
    ))

    plt.savefig(fig_path, bbox_inches='tight')

    debug.print_dictionary(statistics.vars)
