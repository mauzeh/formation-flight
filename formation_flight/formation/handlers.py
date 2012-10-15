from lib import sim
from allocators import * 
from synchronizers import * 
from lib.debug import print_line as p
import config

class FormationHandler(object):

    def __init__(self, allocator, synchronizer):
        sim.dispatcher.register('aircraft-depart', self.handle_departure)
        sim.dispatcher.register('enter-lock-area', self.handle_lock)
        self.allocator = allocator()
        self.synchronizer = synchronizer()

    def handle_departure(self, event):

        aircraft  = event.sender
        allocator = self.allocator
        
        allocator.add_aircraft(aircraft)        
        sim.events.append(sim.Event(
            'enter-lock-area',
            aircraft,
            # If aircraft departs from within lock area, set lock time to now
            sim.time + max(aircraft.time_to_waypoint() - config.lock_time, 0)
        ))

    def handle_lock(self, event):
        
        aircraft  = event.sender
        allocator = self.allocator
        
        # Find the formation having self.
        formation = allocator.find_formation(aircraft)

        # Never try to assign again, even if no formation was found
        allocator.remove_aircraft(aircraft)

        # If no formation is possible
        if not len(formation) > 1:
            p('No formation was possible: %s' % formation)
            return

        p('Formation init: %s' % formation)

        # Remove 'enter-lock-area' events for all buddies
        sim.events = filter(lambda e: e.label != 'enter-lock-area' or
                                      e.sender not in formation, sim.events)

        # Prevent buddies from being assigned somewhere else.
        for buddy in formation:
            # Self was already removed
            if buddy is not aircraft:
                allocator.remove_aircraft(buddy)

        self.synchronizer.synchronize(formation)
