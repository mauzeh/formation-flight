from .point import *
from pydispatch import dispatcher

class Aircraft(object):

    """
    Represents an aircraft.

    Uses the waypoints to fly the aircraft. Waypoints can be dynamically set.
    """

    def __init__(self, name):

        self.name = name
        self.waypoints = []
        self.departure_time = 0

        # km/second
        self.speed = .257222222

        # km/hour
        #self.speed = 926

        self._airtime = 0
        self._current_position = None
        self._current_waypoint = None
        self._previous_waypoint = None
        self._segment_number = 0
        self._initial_bearing = 0
        self._current_bearing = 0
        self._distance_flown = 0
        self._waiting = True


    def get_position(self, time = 0):
        """
        Calculates the position of the aircraft from its starting point.

        Conventions:
        1. Time is in seconds
        2. Lat/lon: 30N 30E = 30 30, but 30S 30W = -30 -30

        """

        # the time that this aircraft has been in flight, from the scheduled
        # moment of departure
        self._airtime = time - self.departure_time

        # determine the total time spent flying all previous segments
        distance_of_previous_segments = 0
        if(self._segment_number > 0):
            self._previous_waypoint = self.waypoints[0]
            for i in range(1, len(self.waypoints)-1):
                waypoint = self.waypoints[i]
                distance_of_previous_segments +=\
                self._previous_waypoint.distance_to(waypoint)
                self._previous_waypoint = waypoint

        time_spent_in_previous_segments = distance_of_previous_segments / self.speed

        # if negative, aircraft waits on ground
        if(self._airtime < 0):
            return -1

        self._previous_waypoint = self.waypoints[self._segment_number]
        self._current_waypoint  = self.waypoints[self._segment_number + 1]

        self._distance_flown = self._airtime * self.speed
        self._distance_flown_in_segment = self.speed *\
                                    (self._airtime -
                                     time_spent_in_previous_segments)
        segment_length = self._previous_waypoint.distance_to(self._current_waypoint)

        if(self._distance_flown_in_segment >= segment_length):

            dispatcher.send(
                'waypoint-reached',
                sender = self,
                time = time,
                data = 'Waypoint "%s" reached' % self._current_waypoint.name
            )

            # No more segments left, so we stop
            if(self._segment_number >= len(self.waypoints)-2):

                dispatcher.send(
                    'destination-reached',
                    sender = self,
                    time = time,
                    data = 'Destination "%s" reached' % self._current_waypoint.name
                )
                return 0

            # Safe to switch to next segment
            self._segment_number = self._segment_number + 1
            self._previous_waypoint = self.waypoints[self._segment_number]
            self._current_waypoint  = self.waypoints[self._segment_number + 1]

        R = Earth.R
        d = self._distance_flown/R
        self._initial_bearing = self._previous_waypoint.bearing_to(self._current_waypoint)

        theta = math.radians(self._initial_bearing)

        lat1 = math.radians(self._previous_waypoint.lat)
        lon1 = math.radians(self._previous_waypoint.lon)

        part1 = math.cos(d) * math.sin(lat1)
        part2 = math.cos(theta) * math.cos(lat1) * math.sin(d)
        lat2  = math.asin(part1 + part2)

        part3 = math.sin(theta) * math.sin(d) * math.cos(lat1)
        part4 = math.cos(d) - math.sin(lat1) * math.sin(lat2)
        lon2  = lon1 + math.atan2(part3, part4)

        # Normalize between -pi and pi
        lon2  = lon2 - 2 * math.pi * math.floor((lon2 + math.pi) / (2 * math.pi))

        # Calculate the end bearing of the aircraft...
        y = math.sin(lon1 - lon2) * math.cos(lat1)
        x = math.cos(lat2) * math.sin(lat1) - math.sin(lat2) *\
                                              math.cos(lat1) *\
                                              math.cos(lon1 - lon2)
        self._current_bearing = (math.degrees(math.atan2(y, x)) + 180) % 360
        self._current_position = Point(math.degrees(lat2), math.degrees(lon2))

        if(self._waiting):
            dispatcher.send(
                'takeoff',
                time = time,
                sender = self,
                data = self
            )
            self._waiting = False

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
