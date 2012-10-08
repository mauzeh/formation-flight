from lib import sim

class Formation(list):
    pass

class FormationHandler(object):

    def __init__(self):
        sim.dispatcher.register('aircraft-depart', self.handle_departure)
        sim.dispatcher.register('formation-lock', self.handle_lock)
        self.aircraft_queue = []
        self.formations = []

    def handle_departure(self, event):
        aircraft = event.sender
        self.aircraft_queue.append(aircraft)
        self.assign()

    def handle_lock(self, event):
        formation = event.sender
        for aircraft in formation:
            self.aircraft_queue.remove(aircraft)

    def assign(self):
        # put all aircraft in one big formation for now.

        # Remove all scheduled 'formation-lock' events because we are re-
        # evaluating the entire set of departed aircraft.
        sim.events.remove_by_label('formation-lock')
        
        self.formations = []
        formation = Formation()
        for aircraft in self.aircraft_queue:
            formation.append(aircraft)
        self.formations.append(formation)

        # Schedule lock events (may be cancelled later)
        # Formation will be locked 10 time units after its creation
        for formation in self.formations:
            sim.events.append(sim.Event(
                'formation-lock',
                formation, 
                sim.time + 10
            ))