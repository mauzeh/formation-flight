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

from lib.geo.util import midpoint
from lib.geo.util import project_segment
from lib.geo.util import reduce_points
from lib.geo.util import point_in_points

import numpy as np

def execute():
    
    # Construct flight list
    planes = generators.get_via_stdin()
    
    hubs         = []
    origins      = []
    destinations = []
    for plane in planes:
        origins.append(plane.origin)
        destinations.append(plane.destination)
    
    print midpoint(origins)
    print midpoint(destinations)