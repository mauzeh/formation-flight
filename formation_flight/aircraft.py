from lib import sim

class Aircraft(object):

    def __init__(self, label = None, route = None, departure_time = 0):

        self.label = label if label is not None else str(route)
        self.route = route
        self.departure_time = departure_time
        self.flight_time = 25

    def depart(self):
        self.arrival_time = sim.time + self.flight_time 
        
    def arrive(self):
        pass

    def __repr__(self):
        return self.label

class AircraftHandler(object):

    def __init__(self):
        sim.dispatcher.register('aircraft-depart', self.handle_departure)
        sim.dispatcher.register('aircraft-arrive', self.handle_arrival)

    def handle_departure(self, event):
        aircraft = event.sender
        aircraft.depart()
        assert hasattr (aircraft, 'arrival_time')
        sim.events.append(sim.Event(
            'aircraft-arrive',
            aircraft,
            aircraft.arrival_time
        ))

    def handle_arrival(self, event):
        aircraft = event.sender
        aircraft.arrive()