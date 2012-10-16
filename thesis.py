#!/usr/bin/env python
"""Simulation bootstrapper"""

import random
import os
import sys
import csv

from optparse import OptionParser

from formation_flight.formation.handlers import FormationHandler
from formation_flight.formation.allocators import *
from formation_flight.formation.synchronizers import *
from formation_flight.aircraft.handlers import AircraftHandler
from formation_flight.aircraft.models import Aircraft
from formation_flight.formation.models import Formation
from lib.geo.route import Route
from lib.geo.waypoint import Waypoint
from lib.geo.point import Point
from lib import sim, debug
from lib.debug import print_line as p

aircraft_handler   = AircraftHandler()
formation_handler  = FormationHandler(
   allocator    = FormationAllocatorEtah,
   synchronizer = FormationSynchronizer
)

# Generate a hub
hubs = [
    Point(54.71, -16.29, 'HUB1'),
    Point(53.22, -17.21, 'HUB2'),
]
planes = []

def parse_options():

    parser = OptionParser()
    parser.add_option("-t", dest="starttime", default = 0,
                      help="The simulation start time (UTC, minutes from midnight).")
    parser.add_option("-d", dest="duration", default = 60,
                      help="The simulation duration (in minutes).")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="don't print status messages to stdout")

    return parser.parse_args()

def init():

    # Initialize settings from command line options
    (options, args) = parse_options()
    starttime = int(options.starttime)
    duration  = int(options.duration)

    # Set up the planes list, assume tab-separated columns via stdin. 
    # Can be piped, example "$ cat data/flights.tsv | ./thesis.py"
    for row in csv.reader(sys.stdin, delimiter = '\t'):

        departure_time = int(row[0])
        label          = row[1]
        waypoints      = row[2].split('-')
        aircraft_type  = row[3]

        planes.append(Aircraft(
            label = label,
            route = Route([
                Waypoint(waypoints[0]), 
                random.choice(hubs), 
                Waypoint(waypoints[1])
            ]),
            departure_time = departure_time,
            aircraft_type = aircraft_type))
        
# Override auto-planes, useful when reproducing a bug...
#planes = [
#    Aircraft('FLT001', Route([Waypoint('DUS'), Waypoint('MAN'),
#        Waypoint('JFK')]), 10),
#    Aircraft('FLT002', Route([Waypoint('FRA'), Waypoint('MAN'),
#        Waypoint('JFK')]), 0),
#    Aircraft('FLT003', Route([Waypoint('BRU'), Waypoint('MAN'),
#        Waypoint('LAX')]), 11),
#    Aircraft('FLT004', Route([Waypoint('BRU'), Waypoint('MAN'),
#        Waypoint('ORD')]), 5),
#    Aircraft('FLT005', Route([Waypoint('DUS'), Waypoint('MAN'),
#        Waypoint('JFK')]), 12),
#    Aircraft('FLT006', Route([Waypoint('AMS'), Waypoint('MAN'),
#        Waypoint('LAX')]), 100),
#    Aircraft('FLT007', Route([Waypoint('BRU'), Waypoint('MAN'),
#        Waypoint('ORD')]), 100),
#    Aircraft('FLT008', Route([Waypoint('CDG'), Waypoint('MAN'),
#        Waypoint('JFK')]), 100),
#]
  
def run():
    init()
    for aircraft in planes:
        sim.events.append(sim.Event(
            'aircraft-depart', 
            aircraft, 
            aircraft.departure_time
        ))

    sim.run()

# docs: http://docs.python.org/library/profile.html
import cProfile, pstats
profile_file = 'data/profile.txt'
cProfile.run('run()', profile_file)
p = pstats.Stats(profile_file)
p.strip_dirs()
#p.sort_stats('cumulative')
p.sort_stats('time')
p.print_stats(30)
