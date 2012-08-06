from .point import *
from pydispatch import dispatcher

class Aircraft(object):

    """
    Represents an aircraft.

    Uses the waypoints to fly the aircraft. Waypoints can be dynamically set.
    """

    def __init__(self, name, route):

        self.name = name
        self.route = route
        self.departure_time = 0

        # km/second
        #self.speed = .257222222

        # km/hour
        #self.speed = 926

        # kts (NM/h)
        # self.speed = 500

        # NM/minute
        self.speed = 600/60

        self._airtime = 0
        self._simtime = 0
        self._current_position = None
        self._waiting = True
        self._landed = False

    def get_position(self, simtime = 0):
        """
        Calculates the position of the aircraft from its starting point.

        Conventions:
        1. Time is in seconds
        2. Lat/lon: 30N 30E = 30 30, but 30S 30W = -30 -30

        """

        # the time that this aircraft has been in flight, from the scheduled
        # moment of departure
        self._simtime = simtime
        self._airtime = simtime - self.departure_time

        if not self.is_in_flight(): return -1

        current_waypoint = self.route.get_current_segment(self.get_distance_flown()).start
        distance_from_current_waypoint = self.route.get_distance_into_current_segment(self.get_distance_flown())

        return self.route.get_current_position(self.get_distance_flown())

        print ''
        print '-------------------------------------------------------'
        print 'airtime: %s' % self._airtime
        print 'current waypoint: %s' % current_waypoint
#        print 'Total flight distance: %s' % self.route.get_length()
#        print 'Segments flown: %s' % self.route.get_segments_flown(self.get_distance_flown())
#        print 'Current Segment: %s' % self.route.get_current_segment(self.get_distance_flown())
#        print 'Distance into current segment: %s km' % self.route.get_distance_into_current_segment(self.get_distance_flown())
#        print self.route.get_segments()

    def get_distance_flown(self):
        return self._airtime * self.speed

    def is_in_flight(self):

        # if negative, aircraft waits on ground
        if self._airtime < 0:
            return False

        # don't even bother if we have landed
        flight_time = self.route.get_length() / self.speed
        if self._airtime > flight_time:
            if not self._landed:
                self._landed = True
                dispatcher.send(
                    'destination-reached',
                    sender = self,
                    #time = simtime,
                    data = 'Destination "%s" reached' % self.route.get_destination()
                )
            return False

        if(self._waiting):
            dispatcher.send(
                'takeoff',
                #time = simtime,
                sender = self,
                data = self
            )
            self._waiting = False
        return True

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
