from lib import sim

class Aircraft(object):

    def __init__(self, label = None, route = None, departure_time = 0):

        self.label = label if label is not None else str(route)
        self.route = route
        self.description = '%s' % route
        self.departure_time = departure_time
        # Distance units per time unit (500 kts)
        self.speed = 500/60

    def depart(self):
        self.position = self.route.waypoints[0]
        del self.route.waypoints[0]
        pass

    def at_waypoint(self):
        self.position = self.route.waypoints[0]
        del self.route.waypoints[0]
        del self.route.segments[0]
        
    def arrive(self):
        pass

    def time_to_waypoint(self):
        waypoint = self.route.waypoints[0]
        distance = self.position.distance_to(waypoint)
        return distance / self.speed

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
        self.clear_events()
        if len(self.aircraft.route.segments) > 1:
            self.schedule_waypoint()
        else:
            self.schedule_arrival()
            
    def add_event(self, event):
        self.events.append(event)
        sim.events.append(event)

    def clear_events(self):
        for event in self.events:
            # @todo, if the event has fired, it mustn't be here in anymore...
            self.events.remove(event)
            # If the event has fired, sim does not have it anymore.
            try:
                sim.events.remove(event)
            except ValueError:
                pass

    def schedule_waypoint(self):
        self.aircraft.waypoint_eta = sim.time + self.aircraft.time_to_waypoint()
        self.add_event(sim.Event(
            'aircraft-at-waypoint',
            self.aircraft,
            self.aircraft.waypoint_eta
        ))

    def schedule_arrival(self):
        self.aircraft.arrival_time = sim.time + self.aircraft.time_to_waypoint()
        self.add_event(sim.Event(
            'aircraft-arrive',
            self.aircraft,
            self.aircraft.arrival_time
        ))
