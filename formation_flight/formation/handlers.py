from lib import sim
from allocators import * 
from synchronizers import * 
from lib.debug import print_line as p

class FormationHandler(object):

    def __init__(self, allocator, synchronizer):
        sim.dispatcher.register('aircraft-depart', self.handle_departure)
        sim.dispatcher.register('formation-lock', self.handle_lock)
        self.allocator = allocator()
        self.synchronizer = synchronizer()

    def handle_departure(self, event):
        aircraft = event.sender
        self.allocator.add_aircraft(aircraft)

        # Remove all scheduled 'formation-lock' events because we are re-
        # evaluating the entire set of departed aircraft.
        p('Trying to remove formation-locks from %s' % sim.events)
#       for e in sim.events:
#           p('Just a loop: %s' % e)
#           if e.label == 'formation-lock':
#               p('Removing %s' % e)
#               sim.events.remove(e)
#           else:
#               pass
#               p('Not removing %s' % e)

        sim.events = filter(lambda e: e.label != 'formation-lock', sim.events)
        
        p('Removed formation-locks from %s' % sim.events)
        self.allocator.assign()

        # Schedule lock events (may be cancelled later)
        # Formation will be locked 10 time units after its creation
        for formation in self.allocator.formations:
            event = sim.Event(
                'formation-lock',
                formation, 
                sim.time + 10
            )
            sim.events.append(event)
            p('Appending %s' % event)

    def handle_lock(self, event):
        formation = event.sender
        p('handling lock for formation: %s' % formation)
        for aircraft in formation:
            p('trying to remove aircraft %s from %s' %\
            (aircraft, self.allocator.aircraft_queue))
            self.allocator.remove_aircraft(aircraft)
        self.synchronizer.synchronize(formation)
