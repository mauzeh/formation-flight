from pydispatch import dispatcher
from formation_flight.aircraft import Aircraft
from formation_flight.waypoint import Waypoint

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

        dispatcher.connect(self.add_to_queue, 'takeoff')

    def add_to_queue(self, signal, sender, data = None, time = 0):

        assert type(sender) == Aircraft
        self.aircraft_queue.append(sender)
        self.execute()

    def execute(self):
        """Assign aircraft in the queue into pending or new formations."""

        # @todo How to balance if we try to compose a new formation and/or add to existing?

        pending_formations = []
        for formation in self.formations:
            if formation.status == 'pending':
                pending_formations.append(formation)

        # Try to create a formation from the queuing aircraft
        for aircraft in self.aircraft_queue:
            pass

        # Find a formation that fits the time window of the current aircraft
        for aircraft in self.aircraft_queue:
            for formation in pending_formations:
                formation_start_point = formation.route[0]
                print(formation_start_point)


        pass