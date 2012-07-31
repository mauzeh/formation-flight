from pydispatch import dispatcher
from formation_flight.aircraft import Aircraft

class Formation(object):
    """Represents a group of aircraft flying together"""

    def __init__(self):

        self.aircraft = []

        # Statuses:
        # pending - Not flying yet, open to receive aircraft
        # active  - Flying. Not open to receive aircraft
        self.status = 'pending'

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
        print sender

    def execute(self):
        """Assign aircraft in the queue into pending or new formations."""

        # @todo How to balance if we try to compose a new formation and/or add to existing?

        for formation in self.formations:
            if formation.status != 'pending': continue

        pass