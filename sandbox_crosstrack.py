from formation_flight.geo import util
from formation_flight.geo.segment import Segment
from formation_flight.geo.point import Point
from formation_flight.geo.waypoint import Waypoint
from formation_flight.geo.route import Route
from formation_flight.aircraft import Aircraft
from lib import combinatorics
import random
from formation_flight import config
    
def is_valid_formation(aircraft_list):

    # Get the segments
    segments = map(lambda aircraft: aircraft.route.segments[0], aircraft_list)

    # Find the reference point collection of segments
    midpoints = map(lambda x: x.midpoint, segments)
    reference = util.midpoint (midpoints)
    deviation_sum = 0
    
    for segment in segments:

        crosstrack = Segment(segment.start, reference)
        
        deviation = util.cross_track_distance (
            crosstrack.get_length(),
            crosstrack.get_initial_bearing(),
            segment.get_initial_bearing()
        )
        deviation_sum = deviation_sum + abs(deviation)

        if abs(deviation) > config.max_deviation:
            return False

        #print '%s (ref = %s) crosstrack distance: %.1f' %\
              #(segment, reference, d_x)

    return deviation_sum

if __name__ == '__main__':

    planes = [
        Aircraft(route = Route([Waypoint('AMS'), Waypoint('JFK')])),
        Aircraft(route = Route([Waypoint('BRU'), Waypoint('BOS')])),
        Aircraft(route = Route([Waypoint('DUS'), Waypoint('MEX')])),
        Aircraft(route = Route([Waypoint('IST'), Waypoint('MEX')])),
        Aircraft(route = Route([Waypoint('CDG'), Waypoint('LAX')])),
        Aircraft(route = Route([Waypoint('TLS'), Waypoint('SFO')])),
    ]

    length = 0

    for n in range(2, len(planes) + 1):

        for subset in combinatorics.k_subsets(planes, n):
            length = length+1
            is_valid = is_valid_formation (subset)
            #if planes[0] in subset:
                #print 'yaaaaaay %s in within %s' % (planes[0], subset)
            if not is_valid: 
                continue
            print '%s, formation: %s' %\
                  (is_valid, subset)
        
    print 'Iterations required: %d' % length

