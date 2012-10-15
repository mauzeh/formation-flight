"""Controllers augment models by changing model data and events."""

from lib import sim

class AircraftController(object):
    """Able to reposition an aircraft and schedule arrival events."""

    def __init__(self, aircraft):
        
        self.aircraft = aircraft
        
        # Keep our own list of all events to prevent lookups in the sim later
        self.aircraft.events = []

    def update_position(self):
        """Calculates the position of the aircraft according to the simtime"""
        flight_time    = sim.time - self.aircraft.departure_time
        distance_flown = flight_time * self.aircraft.speed
        segment        = self.aircraft.route.segments[0]
        self.aircraft.position = segment.start.get_position(
            bearing  = segment.initial_bearing,
            distance = distance_flown
        )

    def calibrate(self):
        """Removes all upcoming events for this aircraft and replans them"""
        self.clear_events()
        if len(self.aircraft.route.segments) > 1:
            self.schedule_waypoint()
        else:
            self.schedule_arrival()
            
    def add_event(self, event):
        self.aircraft.events.append(event)
        sim.events.append(event)

    def clear_events(self):

        for event in self.aircraft.events:

            # Ignore events not pertaining to current aircraft
            # @todo Should not be necessary, right?
            if event.sender is not self.aircraft:
                continue

            # @todo, if the event has fired, it mustn't be here in anymore...
            self.aircraft.events.remove(event)
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
