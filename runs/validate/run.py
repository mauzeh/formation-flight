#!/usr/bin/env python
"""Simulation bootstrapper"""

from formation_flight.formation import handlers as formation_handlers
from formation_flight.aircraft import handlers as aircraft_handlers
from formation_flight.aircraft import generators
from formation_flight.hub import builders
from formation_flight.hub import allocators
from formation_flight import visualization

from formation_flight.aircraft.models import Aircraft
from lib.geo.route import Route
from lib.geo.waypoint import Waypoint

from lib import sim, debug, sink
from lib.debug import print_line as p

from formation_flight import statistics

import config
import os

import numpy as np

def execute():
    single_run()

def single_run():

    sim.init()
    aircraft_handlers.init()
    formation_handlers.init()
    statistics.init()
    #visualization.init()
    
    # Construct flight list
    planes = [
        Aircraft('FLT001', Route([Waypoint('DUS'), Waypoint('IAD')]), 0),
        Aircraft('FLT002', Route([Waypoint('BRU'), Waypoint('ORD')]), 0),
        Aircraft('FLT003', Route([Waypoint('AMS'), Waypoint('IAH')]), 0),
        Aircraft('FLT004', Route([Waypoint('LHR'), Waypoint('ATL')]), 45),
        Aircraft('FLT005', Route([Waypoint('FRA'), Waypoint('SFO')]), 0),
    ]
    
    # Find hubs
    config.hubs = builders.build_hubs(planes, config.count_hubs, config.Z)
    
    # Allocate hubs to flights
    allocators.allocate(planes, config.hubs)
    
    for flight in planes:
        sim.events.append(sim.Event('aircraft-init', flight, 0))
    
    sim.run()

    debug.print_dictionary(statistics.vars)
