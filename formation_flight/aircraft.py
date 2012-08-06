from pydispatch import dispatcher

class Aircraft(object):

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

        # Which segment the aircraft is in. Used to trigger
        # "waypoint-reached" event
        self._segment_index = 0

    def fly(self, simtime = 0):
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

        if not self.is_in_flight(): return False

        self._current_position = self.route.get_current_position(self.get_distance_flown())
        self.has_reached_waypoint()

        if(self._waiting):
            self._waiting = False
            dispatcher.send(
                'takeoff',
                time = self._simtime,
                sender = self,
                data = self
            )

        return True

    def get_position(self):
        return self._current_position

    def get_distance_flown(self):
        return self._airtime * self.speed

    def has_reached_waypoint(self):
        """
        Fires an event each time an aircraft passes a new waypoint

        Assumes that aircraft do not fly past the same waypoint more than once.
        Not even if it is further down the flight.

        If several waypoints are reached at once (can happen with really big
        time intervals) then each waypoint is fired directly after the other.
        """
        current_segment = self.route.get_current_segment(self.get_distance_flown())
        index = self.route.segments.index(current_segment)

        if(index > self._segment_index):
            for i in range(self._segment_index, index):
                segment = self.route.segments[i]
                dispatcher.send(
                    'waypoint-reached',
                    sender = self,
                    time = self._simtime,
                    data = '%s' % segment
                )
        self._segment_index = index

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
                    time = self._simtime,
                    data = 'Destination "%s" reached' % self.route.get_destination()
                )
            return False


        return True

    def __repr__(self):
        #return "%s(%r)" % (self.__class__, self.__dict__)
        return self.name
