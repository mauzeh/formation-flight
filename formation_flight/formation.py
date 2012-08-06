from pydispatch import dispatcher
from formation_flight.aircraft import Aircraft
from formation_flight.geo.waypoint import Waypoint
from lib.intervals import Interval, group

class Formation(object):
    """Represents a group of aircraft flying together"""

    def __init__(self):

        self.aircraft = []

        # Statuses:
        # pending - Not flying yet, open to receive aircraft
        # active  - Flying. Not open to receive aircraft
        self.status = 'pending'

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
        dispatcher.connect(self.synchronize, 'waypoint-reached')

    def assign(self, signal, sender, data = None, time = 0):
        """Assign departing aircraft into pending or new formations."""

        assert type(sender) == Aircraft
        self.aircraft_queue.append(sender)

        # @todo How to balance if we try to compose a new formation and/or add to existing?

        # how much time the arrival at the virtual hub can be delayed/expedited
        # @todo Move this to a central location
        slack = 6

        hub = Waypoint('AMS')

        # Create formations from the queuing aircraft
        intervals = []
        for aircraft in self.aircraft_queue:

            # determine the ETA at the virtual hub
            hub_eta = time + aircraft.get_position().distance_to(hub) / aircraft.speed

            intervals.append(Interval(aircraft.name, int(hub_eta - slack), int(hub_eta + slack)))

#        print group(intervals)

    def synchronize(self, signal, sender, data = None, time = 0):
        """Makes sure that all aircraft in a formation arrive simultaneously"""
        assert type(sender) == Aircraft

        print 't = %.1fs trying to sync %s' % (time, sender)

        # distance to virtual hub
        hub = Waypoint('AMS')
        distance = sender.get_position().distance_to(hub)

        print 'distance to hub %.1f' % distance

        # set speed so that arrival @ hub = 80 units
        time_to_hub = 80 - time
        sender.speed = distance / time_to_hub
