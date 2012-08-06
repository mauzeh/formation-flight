from pydispatch import dispatcher
from formation_flight.aircraft import Aircraft
from formation_flight.waypoint import Waypoint
from lib.intervals import Interval, group

class Formation(object):
    """Represents a group of aircraft flying together"""

    def __init__(self):

        self.aircraft = []

        # Statuses:
        # pending - Not flying yet, open to receive aircraft
        # active  - Flying. Not open to receive aircraft
        self.status = 'pending'

        # The route that the formation is set to fly. Usually contains two waypoints.
        self.route = [Waypoint('AMS'), Waypoint('JFK')]

        # The time at which the formation is set to start
        self.start_time = 0

class Assigner(object):
    """Perform aircraft formation assignment by hooking in to certain simulation events."""

    def __init__(self):

        # List of aircraft that have not been assigned to a formation
        self.aircraft_queue = []

        # List of assigned formations (each containing assigned aircraft)
        self.formations = []

        dispatcher.connect(self.assign, 'takeoff')

    def assign(self, signal, sender, data = None, time = 0):
        """Assign departing aircraft into pending or new formations."""

        assert type(sender) == Aircraft
        self.aircraft_queue.append(sender)

        # @todo How to balance if we try to compose a new formation and/or add to existing?

        # how much time the arrival at the virtual hub can be delayed/expedited
        # @todo Move this to a central location
        slack = 6

        print 'current time: %s' % time

        hub = Waypoint('AMS')

        # Create formations from the queuing aircraft
        intervals = []
        for aircraft in self.aircraft_queue:

            # determine the ETA at the virtual hub
            hub_eta = time + aircraft._current_position.distance_to(hub) / aircraft.speed

            # discard from queue if aircraft is already passed the hub
            #if(hub_eta < time)

#            print 'start point: %s' % aircraft.waypoints[0]
#            print 'start bearing: %s' % aircraft.waypoints[0].bearing_to(aircraft.waypoints[1])
#            print 'current position: %s' % aircraft._current_position
#            print 'distance to hub: %s' % aircraft._current_position.distance_to(hub)
#            print 'hub_eta: %s' % hub_eta
            intervals.append(Interval(aircraft.name, int(hub_eta - slack), int(hub_eta + slack)))

#        print group(intervals)
        print intervals
