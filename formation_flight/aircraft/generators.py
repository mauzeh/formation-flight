import random, csv, sys

import config

from formation_flight.aircraft.models import Aircraft
from lib.geo.route import Route
from lib.geo.waypoint import Waypoint

from lib.debug import print_line as p

def get_manual():

    # Override auto-planes, useful when reproducing a bug...
    return [
        Aircraft('FLT001', Route([Waypoint('FRA'), Waypoint('JFK')]), 12),
        Aircraft('FLT002', Route([Waypoint('FRA'), Waypoint('SFO')]), 12),
        Aircraft('FLT003', Route([Waypoint('CPH'), Waypoint('SFO')]), 57),
        Aircraft('FLT004', Route([Waypoint('AMS'), Waypoint('LAX')]), 59),
    ]

# Keep track of what was passed via stdin for a potential re-init
input_history = []

def get_via_stdin():
    """Set up the planes list, assume tab-separated columns via stdin.
    Can be piped, example: $ cat data/flights.tsv | ./thesis.py"""
    
    planes = []

    if len(input_history) == 0:
        for row in csv.reader(sys.stdin, delimiter = '\t'):
            input_history.append(row)

    for row in input_history:

        departure_time = int(row[0])
        label          = row[1]
        waypoints      = row[2].split('-')
        aircraft_type  = row[3]

        # If a flight has been calibrated, the formation probability will be
        # given. Otherwise it will be set to None.
        try:
            probability = float(row[4])
            # Disregard row if config tells us to
            if probability < config.min_P:
                p('Probability of row does not match criterium %s, row %s' % (
                    config.min_P,
                    row
                ))
                continue
        except IndexError:
            probability = None
            
        # Keep track of scheduled departure time for later retrieval
        departure_time_scheduled = departure_time
        
        # Departure times are randomly distributed
        # In some rare cases (only for early aircraft) the departure time might
        # become negative so we restrict it to being only positive
        departure_time = departure_time +\
            random.uniform(max(0, -1 * config.dt), config.dt)

        aircraft = Aircraft(
            label = label,
            route = Route([
                Waypoint(waypoints[0]),
                Waypoint(waypoints[1])
            ]),
            departure_time = departure_time,
            aircraft_type = aircraft_type)

        aircraft.departure_time_scheduled = departure_time_scheduled
        
        # If a flight has been calibrated, the formation probability will be
        # given. Otherwise it will be set to None.
        aircraft.probability = probability

        ## Find a random hub
        #hub = random.choice(config.hubs),

        ## Find the closest hub
        #hub = min(config.hubs, key = lambda x: x.distance_to(aircraft.origin))

        planes.append(aircraft)

    return planes