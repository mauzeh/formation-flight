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

# Overwrite default configuration values
config.alpha      = .13
config.etah_slack = 50
config.lock_time  = 10
config.phi_max    = 5
config.Z          = .25
config.departure_distribution = {
    'type'        : 'uniform',
    'lower_bound' : -10,
    'upper_bound' : 10
}

# Create custom set of hubs
lats = np.mgrid[ 40: 70: 2j]
lons = np.mgrid[-60: 25: 2j]

config.hubs = []
for lat in lats:
    for lon in lons:
        config.hubs.append(Point(lat, lon))

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

def execute():
    
    print 'init sink %s' % config.sink_dir
    
    sink.init(config.sink_dir)

    for hub in config.hubs:
        
        print 'Progress: %d of %d iterations' % (
            config.hubs.index(hub)+1,
            len(config.hubs)
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
