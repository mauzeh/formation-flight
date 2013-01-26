#!/usr/bin/env python
"""Simulation bootstrapper"""

from formation_flight.formation import handlers as formation_handlers
from formation_flight.aircraft import handlers as aircraft_handlers
from formation_flight.aircraft import generators
from formation_flight.hub import builders
from formation_flight.hub import allocators

from lib import sim, debug, sink
from lib.debug import print_line as p

from formation_flight import statistics

import config
import os

import numpy as np

def init():    
    sink.init(config.sink_dir)

def execute():
    init()
    single_run()

def single_run():
    
    sim.init()
    aircraft_handlers.init()
    formation_handlers.init()
    statistics.init()
    #plot.init()
    
    # Construct flight list
    planes = generators.get_via_stdin()
    #planes = generators.get_manual()
    
    if len(planes) > 0:

        # Find hubs
        config.hubs = builders.build_hubs(planes, config.count_hubs, config.Z)
    
        # Allocate hubs to flights
        allocators.allocate(planes, config.hubs)
        
        for flight in planes:
            sim.events.append(sim.Event('aircraft-init', flight, 0))
        
    sim.run()

    sink.push(statistics.vars)
    debug.print_dictionary(statistics.vars)
    

