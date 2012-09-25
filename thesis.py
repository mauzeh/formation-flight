#!/usr/bin/env python
import os
import csv

from formation_flight.aircraft import Aircraft
from formation_flight.geo.route import Route
from formation_flight.geo.waypoint import Waypoint
from formation_flight import simulator
from lib import debug
from formation_flight import formation, virtual_hub

if __name__ == '__main__':

    # Initialize event listeners
    virtual_hub.register()
    formation.register()
    debug.register()

    # Read the data file containing a list of flights and set up the
    # planes list
    fn = os.path.join(os.path.dirname(__file__), 'data/flights.csv')
    planes = []

    for row in csv.reader(open(fn)):

        waypoints = []

        for point in row[3].split('-'):
            waypoints.append(Waypoint(point))
            
        route          = Route(waypoints)
        departure_time = int(row[2])
        aircraft       = Aircraft(row[0], route, departure_time)
        planes.append(aircraft)

    simulator.execute(range(0, 120, 1), planes)

    # Example syntax
    # route = Route([Waypoint('CDG'),
    #                Waypoint('AMS'),
    #                Waypoint('MCO')])
    # aircraft = Aircraft("CDG-AMS-MCO", route)
    # aircraft.departure_time = 5
    # planes.append(aircraft)

    # docs: http://docs.python.org/library/profile.html
    # import cProfile, pstats
    # profile_file = 'data/profile.txt'
    # cProfile.run('run()', profile_file)
    # p = pstats.Stats(profile_file)
    # p.strip_dirs()
    # p.sort_stats('cumulative')
    # p.print_stats(15)