#!/usr/bin/env python

import random

from formation_flight.formation import FormationHandler
from formation_flight.aircraft import Aircraft, AircraftHandler
from lib.geo.route import Route
from lib.geo.waypoint import Waypoint
from lib import sim

aircraft_handler   = AircraftHandler()
formation_assigner = FormationHandler()

# Generate a big list of random flights
origins      = ['AMS', 'CDG', 'LHR', 'FRA', 'DUS', 'BRU']
destinations = ['EWR', 'JFK', 'ORD', 'LAX', 'SFO']
hubs         = ['MAN', 'LHR']
planes       = []

for i in range(0, 500):
    planes.append(Aircraft(
        label = 'FLT%03d' % i,
        route = Route([
            Waypoint(random.choice(origins)), 
            Waypoint(random.choice(destinations))
        ]),
        departure_time = random.choice(range(450, 600))))

# Override auto-planes, useful when reproducing a bug...
#planes = [
#    Aircraft('FLT001', Route([Waypoint('AMS'), Waypoint('MAN'), Waypoint('LAX')]), 18),
#    Aircraft('FLT001', Route([Waypoint('BRU'), Waypoint('MAN'), Waypoint('SFO')]), 18),
#    Aircraft('FLT001', Route([Waypoint('CDG'), Waypoint('MAN'), Waypoint('ORD')]), 18),
#]
        
def run():

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
