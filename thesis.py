#!/usr/bin/env python
import os
import sys
import csv

from optparse import OptionParser

from formation_flight import diag
from formation_flight.aircraft import Aircraft
from formation_flight.geo.route import Route
from formation_flight.geo.waypoint import Waypoint
from formation_flight import simulator
from formation_flight import formation, virtual_hub

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

def run():

    # Initialize settings from command line options
    (options, args) = parse_options ()
    starttime = int(options.starttime)
    duration  = int(options.duration)
        
    # Initialize event listeners
    virtual_hub.register()
    formation.register()
    diag.register()

    # Set up the planes list, assume tab-separated columns via stdin. 
    # Can be piped, example "$ cat flights.tsv | ./thesis.py"
    planes = []
    for row in csv.reader(sys.stdin, delimiter = '\t'):

        departure_time = row[0]
        label          = row[1]
        od_pair        = row[2]
        aircraft_type  = row[3]

        waypoints = []

        for point in od_pair.split('-'):
            waypoints.append(Waypoint(point))
            
        route          = Route(waypoints)
        departure_time = int(departure_time)
        aircraft       = Aircraft(label, route, departure_time)
        planes.append(aircraft)

    simulator.execute(range(starttime, starttime + duration, 1), planes)

# docs: http://docs.python.org/library/profile.html
import cProfile, pstats
profile_file = 'data/profile.txt'
cProfile.run('run()', profile_file)
p = pstats.Stats(profile_file)
p.strip_dirs()
#p.sort_stats('cumulative')
p.sort_stats('time')
p.print_stats(15)