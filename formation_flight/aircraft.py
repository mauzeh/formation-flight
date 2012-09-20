from pydispatch import dispatcher
from formation_flight import simulator

class Aircraft(object):

    def __init__(self, name, route, departure_time):

        self.name = name
        self.route = route
        self.departure_time = departure_time

        # km/second
        #self.speed = .257222222

        # km/hour
        #self.speed = 926

        # kts (NM/h)
        # self.speed = 500

        # KM/minute
        self.speed = 10

        self._airtime = 0
        self._simtime = 0
        self._current_position = None
        self._distance_flown = 0
        self._waiting = True
        self._landed = False

        # Which segment the aircraft is in. Used to trigger
        # "waypoint-reached" event
        self._segment_index = 0

    def fly(self):
        """
        Calculates the position of the aircraft from its starting point.

        Conventions:
        1. Time is in seconds
        2. Lat/lon: 30N 30E = 30 30, but 30S 30W = -30 -30

        """
        self.set_time()

        if not self.is_in_flight(): return False

        self._current_position = self.route.get_current_position(
            self.get_distance_flown())
        self.has_reached_waypoint()

        # self._waiting is True by default and needs to be set to False once
        # we switch to being 'in flight'.
        if(self._waiting):
            self._waiting = False
            dispatcher.send(
                'takeoff',
                time = simulator.get_time(),
                sender = self,
                data = self
            )
        else:
            # Nothing weird is happening, no take-off, no landing, just fly.
            dispatcher.send(
                'fly',
                time = simulator.get_time(),
                sender = self,
                data = self
            )

        return True

    def set_time(self):

        # the time that this aircraft has been in flight, from the scheduled
        # moment of departure
        previous_airtime = self._airtime
        self._airtime    = simulator.get_time() - self.departure_time
        self._time_delta = self._airtime - previous_airtime
        self._distance_flown = self._distance_flown +\
                               self.speed * self._time_delta

    def get_position(self):
        return self._current_position

    def get_distance_flown(self):
        return self._distance_flown

    def get_current_waypoint(self):
        segment = self.route.get_current_segment(self.get_distance_flown())
        return segment.end

    def get_waypoint_eta(self):

        segment = self.route.get_current_segment(self.get_distance_flown())
        l       = segment.get_length()
        d       = self.route.get_distance_into_current_segment(
                    self.get_distance_flown())
        eta     = simulator.get_time() + (l - d) / self.speed
        return eta

    def has_reached_waypoint(self):
        """
        Fires an event each time an aircraft passes a new waypoint

        Assumes that aircraft do not fly past the same waypoint more than once.
        Not even if it is further down the flight.

        If several waypoints are reached at once (can happen with really big
        time intervals) then each waypoint is fired directly after the other.
        """
        distance_flown = self.get_distance_flown()
        current_segment = self.route.get_current_segment(distance_flown)
        index = self.route.segments.index(current_segment)

        if(index > self._segment_index):
            for i in range(self._segment_index, index):
                segment = self.route.segments[i]
                dispatcher.send(
                    'waypoint-reached',
                    sender = self,
                    time = simulator.get_time(),
                    data = self
                )
        self._segment_index = index

    def is_in_flight(self):

        # if negative, aircraft waits on ground
        if self._airtime < 0:
            return False

        # don't even bother if we have landed
        if self.get_distance_flown() > self.route.get_length():
            if not self._landed:
                self._landed = True
                dispatcher.send(
                    'destination-reached',
                    sender = self,
                    time = simulator.get_time(),
                    data = 'Destination "%s" reached' %
                           self.route.get_destination()
                )
            return False

        return True

    def __repr__(self):
        #return "%s(%r)" % (self.__class__, self.__dict__)
        return self.name
