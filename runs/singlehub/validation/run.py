#!/usr/bin/env python
"""Simulation bootstrapper for contour plot"""

from formation_flight.formation import handlers as formation_handlers
from formation_flight.aircraft import handlers as aircraft_handlers
from formation_flight.aircraft import generators
from formation_flight.hub import builders
from formation_flight.hub import allocators
from formation_flight import visualization

from lib import sim, debug, sink
from lib.debug import print_line as p

from formation_flight import statistics

import config
import os

from lib.geo.point import Point
from lib.geo.waypoint import Waypoint
from formation_flight.aircraft.models import Aircraft
from lib.geo.route import Route

import numpy as np

hub = Waypoint('DUB')
hub.origins = [Waypoint('LHR')]

config.hubs = []
config.hubs.append(hub)

def execute():

    for hub in config.hubs:

        sim.init()
        aircraft_handlers.init()
        formation_handlers.init()
        statistics.init()
        visualization.init()

        # Construct flight list
        planes = [
            Aircraft('FLT001', Route([Waypoint('LHR'), Waypoint('IAD')]), 0),
            Aircraft('FLT001', Route([Waypoint('LHR'), Waypoint('IAD')]), 0),
            Aircraft('FLT001', Route([Waypoint('LHR'), Waypoint('IAD')]), 0),
            Aircraft('FLT002', Route([Waypoint('LHR'), Waypoint('JFK')]), 0),
            #Aircraft('FLT003', Route([Waypoint('LHR'), Waypoint('SFO')]), 0),
            Aircraft('FLT003', Route([Waypoint('LHR'), Waypoint('ORD')]), 0),
        ]

        # Allocate hubs to flights
        allocators.allocate(planes, config.hubs)
        
        for flight in planes:
            sim.events.append(sim.Event('aircraft-init', flight, 0))

        sim.run()

        debug.print_dictionary(statistics.vars)