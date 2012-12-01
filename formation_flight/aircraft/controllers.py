"""Controllers augment models by changing model data and events."""

from lib import sim
from lib.debug import print_line as p

class AircraftController(object):
    """Able to reposition an aircraft and schedule arrival events."""

    def __init__(self, aircraft):
        
        self.aircraft = aircraft
        
        # Keep our own list of all events to prevent lookups in the sim later
        self.aircraft.events = []

    def update_position(self):
        """Calculates the position of the aircraft according to the simtime"""
        # Assume that the flight has been properly set up with a hub.
        assert len(self.aircraft.route.segments) > 0
        flight_time    = sim.time - self.aircraft.departure_time
        distance_flown = flight_time * self.aircraft.speed
        segment        = self.aircraft.route.segments[0]
        new_pos        = segment.start.get_position(
            bearing  = segment.initial_bearing,
            distance = distance_flown
        )
        p('Updating position of %s from %s to %s (d_flown=%d, flt_time=%d)' % (
            '%s (%s)' % (self.aircraft, self.aircraft.route.segments),
            self.aircraft.position,
            new_pos,
            distance_flown,
            flight_time
        ))
        self.aircraft.position = new_pos

    def calibrate(self):
        """Removes all upcoming events for this aircraft and replans them"""
        self.clear_events()
        if len(self.aircraft.route.waypoints) > 1:
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
            
    def delay_events(self, delay):
        
        p('Delaying all events for aircraft %s by delay = %s.' % (
            self.aircraft, delay
        ))
        p('Event list before delayal: %s' % self.aircraft.events)

        # Quick an dirty: expose delay for statistics.
        # @todo decouple. Idea: create a separate delay event that sends the
        # amount this aircraft was delayed to anybody who listens?
        # In order to make this quick-and-dirty fix bug free, we can only
        # delay an aircraft once in its lifetime to prevent the variable being
        # overwritten by multiple calls to this methods.
        assert not hasattr(self.aircraft, 'hub_delay')
        self.aircraft.hub_delay = delay

        if hasattr(self.aircraft, 'waypoint_eta'):
            self.aircraft.waypoint_eta = self.aircraft.waypoint_eta + delay
        if hasattr(self.aircraft, 'arrival_time'):
            self.aircraft.arrival_time = self.aircraft.arrival_time + delay
        for event in self.aircraft.events:
            event.time = event.time + delay
        p('Event list after delayal: %s' % self.aircraft.events)
    
    def schedule_departure(self):
        self.add_event(sim.Event(
            'aircraft-depart',
            self.aircraft,
            self.aircraft.departure_time
        ))

    def schedule_waypoint(self):
        self.aircraft.waypoint_eta = sim.time + self.aircraft.time_to_waypoint()
        p('Schedule waypoint-arrive. WP: %s. ETA: %d. Aircraft: %s' % (
            self.aircraft.route.waypoints[0],
            self.aircraft.waypoint_eta,
            self.aircraft
            ))
        self.add_event(sim.Event(
            'aircraft-at-waypoint',
            self.aircraft,
            self.aircraft.waypoint_eta
        ))

    def schedule_arrival(self):
        self.aircraft.arrival_time = sim.time + self.aircraft.time_to_waypoint()
        p('Scheduling arrival of aircraft %s at destination %s at time %s' %\
          (
            self.aircraft,
            self.aircraft.destination,
            self.aircraft.arrival_time,
        ))
        
        self.add_event(sim.Event(
            'aircraft-arrive',
            self.aircraft,
            self.aircraft.arrival_time
        ))
