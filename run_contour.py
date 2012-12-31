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

from lib.geo.point import Point
from lib.geo.waypoint import Waypoint

# Create custom set of hubs
hubs = [
    Point(60, -30), Point(60, -20), Point(60, -10), 
    Point(50, -30), Point(50, -20), Point(50, -10), 
    Point(40, -30), Point(40, -20), Point(40, -10), 
]

def run():
    
    sink.init('data/sink.tsv')

    for hub in hubs:

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
            'hub_lat' : hub.lat,
            'hub_lon' : hub.lon,
            'success_rate' : statistics.vars['formation_success_rate']
        }

        sink.push(d)
        debug.print_dictionary(d)

        #debug.print_dictionary(statistics.vars)
        #sink.push(statistics.vars)

run()