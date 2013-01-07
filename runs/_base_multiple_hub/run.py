#!/usr/bin/env python
"""Simulation bootstrapper"""

from formation_flight.formation import handlers as formation_handlers
from formation_flight.aircraft import handlers as aircraft_handlers
from formation_flight.aircraft import generators
from formation_flight.hub import builders
from formation_flight.hub import allocators

from lib import sim, debug, sink
from lib.debug import print_line as p

import plot
from formation_flight import statistics

import config
import os

import numpy as np

# Overwrite default configuration values
config.alpha      = .13
config.etah_slack = 3
config.lock_time  = 10
config.phi_max    = 5
config.count_hubs = 2
config.Z          = .25
config.departure_distribution = {
    'type'        : 'uniform',
    'lower_bound' : -10,
    'upper_bound' : 10
}

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

def execute():

    sink.init(config.sink_dir)

    for i in np.arange(0, 1, 1):
        
        sim.init()
        aircraft_handlers.init()
        formation_handlers.init()
        statistics.init()
        #plot.init()
        
        # Construct flight list
        planes = generators.get_via_stdin()
        
        # Find hubs
        hubs = builders.build_hubs(planes, config.count_hubs, config.Z)
        
        # Allocate hubs to flights
        allocators.allocate(planes, hubs)
        
        for flight in planes:
            sim.events.append(sim.Event('aircraft-init', flight, 0))
        
        sim.run()

        sink.push(statistics.vars)
        debug.print_dictionary(statistics.vars)
