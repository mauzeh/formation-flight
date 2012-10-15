from lib import sim
from allocators import * 
from synchronizers import * 
from lib.debug import print_line as p

class FormationHandler(object):

    def __init__(self, allocator, synchronizer):
        sim.dispatcher.register('aircraft-depart', self.handle_departure)
        self.allocator = allocator()
        self.synchronizer = synchronizer()

    def handle_departure(self, event):
        aircraft = event.sender
        self.allocator.add_aircraft(aircraft)

    def handle_lock(self, event):
        formation = event.sender
        for aircraft in formation:
            self.allocator.remove_aircraft(aircraft)
        self.synchronizer.synchronize(formation)
