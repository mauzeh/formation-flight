from lib import sim

class Aircraft(object):

    def __init__(self, label = None, route = None, departure_time = 0):

        self.label = label if label is not None else str(route)
        self.route = route
        self.departure_time = departure_time
        self.flight_time = 25

    def depart(self):
        pass

    def at_waypoint(self):
        pass
        
    def arrive(self):
        pass

    def __repr__(self):
        return self.label

class AircraftHandler(object):

    def __init__(self):
        sim.dispatcher.register('aircraft-depart', self.handle_departure)
        sim.dispatcher.register('aircraft-at-waypoint', self.handle_waypoint)
        sim.dispatcher.register('aircraft-arrive', self.handle_arrival)

    def handle_departure(self, event):
        aircraft = event.sender
        aircraft.depart()
        aircraft.controller = AircraftController(aircraft)
        aircraft.controller.calibrate()

    def handle_waypoint(self, event):
        aircraft = event.sender
        aircraft.at_waypoint()
        aircraft.controller.calibrate()

    def handle_arrival(self, event):
        aircraft = event.sender
        aircraft.arrive()

class AircraftController(object):

    def __init__(self, aircraft):
        
        self.aircraft = aircraft
        
        # Keep our own list of all events to prevent lookups in the sim later
        self.events = []

    def calibrate(self):
        """Removes all upcoming events for this aircraft and replans them"""
        self.schedule_arrival()

    def clear_events(self):
        for event in self.events:
            del self.events[event]
            del sim.events[event]

    def schedule_arrival(self):
        self.aircraft.arrival_time = sim.time + self.aircraft.flight_time
        event = sim.Event(
            'aircraft-arrive',
            self.aircraft,
            self.aircraft.arrival_time
        )
        self.events.append(event)
        sim.events.append(event)