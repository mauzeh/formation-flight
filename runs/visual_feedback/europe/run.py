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

# Single hub case
config.count_hubs = 1
config.min_P = 0.3
config.dt = 0
config.Z = 0.12
config.phi_max = 15
config.etah_slack = 30

# Dual hub case
# Call this with:
# $ cat data/calibrated.tsv | egrep -v '(AGP)' | ./run.py
config.count_hubs = 2
config.min_P = 0.12
config.dt = 0
config.Z = 0.12
config.phi_max = 15
config.etah_slack = 30

config.map_dimensions = {
    'lat' : [ 35., 70.],
    'lon' : [-20., 20.]
}

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

def create_segments(flights):
    
    segments = {
        'benchmark' : [],
        'formation' : [],
        'solo'      : []
    }

    for aircraft in flights:
        
        # Temp for timing analysis (no formations yet)
        # We place these segment in the formation var so that the lines are
        # nice and green
        #segments['formation'].append(Segment(aircraft.origin, aircraft.hub))
        #segments['formation'].append(Segment(aircraft.hub, aircraft.destination))
        #return
        
        if hasattr(aircraft, 'formation'):
            segments['formation'].append(Segment(aircraft.origin, aircraft.hub))
            segments['formation'].append(Segment(aircraft.hub, aircraft.hookoff_point))
            segments['formation'].append(Segment(aircraft.hookoff_point, aircraft.destination))
        else:
            # Note: not all aircraft fly via the hub. If their origin is within the
            # lock area, they fly directly to the destination
            route = Route(aircraft.waypoints_passed)
            for segment in route.segments:
                segments['solo'].append(segment)
    
    return segments

def execute():

    planes = run.single_run()
    
    segments = create_segments(planes)

    plt, ax = run.render(segments)

    name = 'count_hubs_%d' % config.count_hubs
    fig_path = '%s/plot_%s.pdf' % (config.sink_dir, name)
    fig_path = fig_path.replace('/runs/', '/plots/')
    fig_path = fig_path.replace('/sink/', '/')

    make_sure_path_exists(os.path.dirname(fig_path))
    
    plt.title(r'$H=%d$, $Z=%.2f$, $S_f=%.2f$' % (
        config.count_hubs,
        config.Z,
        statistics.vars['formation_success_rate']
    ))
    #plt.show()
    plt.savefig(fig_path, bbox_inches='tight')
