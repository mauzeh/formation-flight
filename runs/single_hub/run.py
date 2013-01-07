#!/usr/bin/env python
"""Simulation bootstrapper for contour plot"""

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

from lib.geo.point import Point
from lib.geo.waypoint import Waypoint

import numpy as np

# Create custom set of hubs
lats = np.mgrid[ 40: 70: 2j]
lons = np.mgrid[-60: 25: 2j]

hubs = []
for lat in lats:
    for lon in lons:
        hubs.append(Point(lat, lon))

# Keep this here for debug purposes
#hubs = [
#    Point(60, -30), Point(60, -20), Point(60, -10), 
#    Point(50, -30), Point(50, -20), Point(50, -10), 
#    Point(40, -30), Point(40, -20), Point(40, -10), 
#]

def execute():
    
    sink.init(os.path.dirname(__file__))

    for hub in hubs:
        
        print 'Progress: %d of %d iterations' % (
            hubs.index(hub)+1,
            len(hubs)
        )

        sim.init()
        aircraft_handlers.init()
        formation_handlers.init()
        statistics.init()
        
        # Construct flight list
        planes = generators.get_via_stdin()
        
        # Allocate hubs to flights
        for flight in planes:

            # Assign hub by injecting into route
            flight.route.waypoints = [
                flight.route.waypoints[0],
                hub,
                flight.route.waypoints[1]
            ]
    
            flight.route.init_segments()
        
        for flight in planes:
            sim.events.append(sim.Event('aircraft-init', flight, 0))

        sim.run()

        # Prepare data matrix
        d = {
            'hub_lat'                : hub.lat,
            'hub_lon'                : hub.lon,
            'distance_total'         : float(statistics.vars['distance_total']),
            'distance_formation'     : float(statistics.vars['distance_formation']),
            'distance_solo'          : float(statistics.vars['distance_solo']),
            'formation_count'        : float(statistics.vars['formation_count']),
            'formation_success_rate' : float(statistics.vars['formation_success_rate']),
            'alpha_eff'              : float(statistics.vars['alpha_effective']),
            'distance_success_rate'  : float(statistics.vars['distance_success_rate']),
        }

        sink.push(d)
        debug.print_dictionary(d)

        #debug.print_dictionary(statistics.vars)
        #sink.push(statistics.vars)
