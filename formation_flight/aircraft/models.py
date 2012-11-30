"""Models contain information and do not initiate actions or commands."""
from lib.debug import print_line as p
from lib.geo.route import Route
from lib import sim

class Aircraft(object):
    """An individual flight."""

    def __init__(self, label = None, route = None,
                 departure_time = 0, aircraft_type = None):

        self.label = label if label is not None else str(route)
        self.route = route
        self.waypoints_passed = []
        self.description = str(route)
        self.departure_time = departure_time
        self.aircraft_type = aircraft_type
        self.origin = self.route.waypoints[0]
        self.destination = self.route.waypoints[-1]
        # Distance units per time unit (500 kts)
        self.speed = 500/60
        # Temporary, set speed to 1 for easy manual distance/time verification
        #self.speed = 1

    def depart(self):
        """Sets the current position and increments to the first waypoint."""
        self.position = self.route.waypoints[0]
        self.waypoints_passed.append(self.position)
        p('Deleting waypoint %s from %s due to %s  of aircraft %s' %\
          (self.position, self.route, 'departure', self))
        del self.route.waypoints[0]
        # Do not delete first segment, so segments[0] should always contain
        # the currently active segment
        #del self.route.segments[0]

    def at_waypoint(self):
        """Sets the current position and increments to the next segment."""
        self.position = self.route.waypoints[0]
        self.waypoints_passed.append(self.position)
        p('Deleting waypoint %s from %s due to %s of aircraft %s' %\
          (self.position, self.route, 'waypoint-reach', self))
        del self.route.waypoints[0]
        del self.route.segments[0]
        
    def arrive(self):
        """Placeholder for the aircraft's arrival."""
        self.position = self.route.waypoints[0]
        self.waypoints_passed.append(self.position)
        p('Deleting waypoint %s from %s due to %s of aircraft %s' %\
          (self.position, self.route, 'arrival', self))
        del self.route.waypoints[0]

    def time_to_waypoint(self):
        """Calculates the time left to fly to the current waypoint."""
        waypoint = self.route.waypoints[0]
        distance = self.position.distance_to(waypoint)
        ttwp = distance / self.speed
        p('Time to waypoint %s (d=%d, curtime=%d) for aircraft %s (v=%s, pos=%s) = %d' % (
            '%s {%d, %d}' % (waypoint, waypoint.lat, waypoint.lon),
            distance,
            sim.time,
            self,
            self.speed,
            '{%d, %d}' % (self.position.lat, self.position.lon),
            ttwp
        ))
        return ttwp

    def __repr__(self):
        return '%s (%s-%s, t=%d)' %\
        (
            self.label,
            #self.aircraft_type,
            self.origin,
            self.destination,
            self.departure_time
        )
    
