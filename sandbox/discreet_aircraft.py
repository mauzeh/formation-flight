time = 0

class EventList(list):

    def remove_by_label(self, label):
        for event in self:
            if event.label == label:
                self.remove(event)

events = EventList()

class SimObject(object):
    def __init__(self, label):
        self.label = label
    def __repr__(self):
        return self.label

class Aircraft(SimObject):

    def __init__(self, label):
        self.label = label
        self.flight_time = 25

    def depart(self):
        self.arrival_time = time + self.flight_time 
        
    def arrive(self):
        pass

class Formation(list):
    pass

class Event(object):
    
    def __init__(self, label, sender, bubble_time = 0):

        assert bubble_time >= time

        self.label = label
        self.sender = sender
        self.time = bubble_time

    def __repr__(self):
        return self.label
        
    def __cmp__(self, other):
        """Allows for easy retrieval of earliest elements (having min(time))"""
        try:
            return cmp(self.time, other.time)
        except AttributeError:
            print 'hmmmm %s versus %s' % (self, other)

class Dispatcher(object):

    def __init__(self):
        self.listeners = {}

    def register(self, event_label, listener):
        if event_label not in self.listeners:
            self.listeners[event_label] = []
        self.listeners[event_label].append(listener)

    def bubble(self, event):
        log_event(event)
        if event.label not in self.listeners:
            return
        for listener in self.listeners[event.label]:
            listener(event)

class AircraftHandler(object):

    def handle_departure(self, event):
        aircraft = event.sender
        aircraft.depart()
        assert hasattr (aircraft, 'arrival_time')
        events.append(Event(
            'aircraft-arrive',
            aircraft,
            aircraft.arrival_time
        ))

    def handle_arrival(self, event):
        aircraft = event.sender
        aircraft.arrive()
            
class FormationAssigner(object):

    def __init__(self):
        self.aircraft_queue = []
        self.formations = []

    def handle_departure(self, event):
        aircraft = event.sender
        self.aircraft_queue.append(aircraft)
        self.assign()

    def assign(self):
        # put all aircraft in one big formation for now.

        # Remove all scheduled 'formation-lock' events because we are re-
        # evaluating the entire set of departed aircraft.
        events.remove_by_label('formation-lock')

        self.formations = []
        formation = Formation()
        for aircraft in self.aircraft_queue:
            formation.append(aircraft)
        self.formations.append(formation)

        # Schedule lock events (may be cancelled later)
        # Formation will be locked 10 time units after its creation
        for formation in self.formations:
            events.append(Event('formation-lock', formation, time + 10))

def log_event(event):
    print 't=% 5d: % 25s (%s)' % (event.time, event, event.sender)

formation_assigner = FormationAssigner()
aircraft_handler = AircraftHandler()

dispatcher = Dispatcher()
dispatcher.register('aircraft-depart', aircraft_handler.handle_departure)
dispatcher.register('aircraft-depart', formation_assigner.handle_departure)
dispatcher.register('aircraft-arrive', aircraft_handler.handle_arrival)

def run():

    for i in range(100):
        events.append(Event('aircraft-depart', Aircraft('BRU-LHR'), i + 10))

    while len(events) > 0:
        event = min(events)
        key = events.index(event)
        del events[key]
        time = event.time
        dispatcher.bubble(event)

# docs: http://docs.python.org/library/profile.html
import cProfile, pstats
profile_file = 'data/profile.txt'
cProfile.run('run()', profile_file)
p = pstats.Stats(profile_file)
p.strip_dirs()
#p.sort_stats('cumulative')
p.sort_stats('time')
p.print_stats(30)