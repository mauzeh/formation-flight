"""Handlers listen and react to events."""

from lib import sim
from allocators import * 
from synchronizers import * 
from lib.debug import print_line as p
import config

class FormationHandler(object):
    """Uses the aircraft-depart event to initiate formation allocation"""

    def __init__(self, allocator, synchronizer):
        sim.dispatcher.register('aircraft-depart', self.handle_departure)
        sim.dispatcher.register('enter-lock-area', self.handle_lock)
        sim.dispatcher.register('formation-alive', self.handle_alive)
        self.allocator = allocator()
        self.synchronizer = synchronizer()

    def handle_departure(self, event):
        """Adds the aircraft to the candidate stack and schedules lock event."""

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
        """Upon lock, find a formation (if exists) for current aircraft."""

        aircraft  = event.sender
        allocator = self.allocator
        
        # Find the formation having self.
        formation = allocator.find_formation(aircraft)

        # Never try to allocate again, even if no formation was found
        allocator.remove_aircraft(aircraft)

        # If no formation is possible
        if not len(formation) > 1:
            p('No formation was possible: %s' % formation)
            return

        # Register which hub this formation belongs to
        formation.hub = formation[0].route.waypoints[0]

        p('Formation init: %s' % formation)

        # Remove 'enter-lock-area' events for all buddies
        sim.events = filter(lambda e: e.label != 'enter-lock-area' or
                                      e.sender not in formation, sim.events)

        # Prevent buddies from being allocated somewhere else.
        for buddy in formation:
            # Self was already removed
            if buddy is not aircraft:
                allocator.remove_aircraft(buddy)

        self.synchronizer.synchronize(formation)

    def handle_alive(self, event):
        """Initialize the formation and determine hookoff points."""

        # @todo do we need this? maybe remove?
        # @todo move to class similar to statistics.py?
        # Create a formation id to be used in the data sink.
        if not hasattr(self, 'formation_count'):
            self.formation_count = 0
        self.formation_count = self.formation_count + 1
        formation = event.sender
        formation.id = self.formation_count

        # Tell aircraft in which formation it is flying.
        # @todo move to class similar to statistics.py?
        for aircraft in formation:
            aircraft.formation = formation

        # Determine formation trunk route
        # @todo make midpoint dynamic.
        from lib.geo.waypoint import Waypoint
        from lib.geo.segment import Segment
        from lib.geo.util import project_segment, get_hookoff_quotient
        arrival_midpoint = Waypoint('BOS')
        trunk_segment = Segment(formation.hub, arrival_midpoint)

        # Determine hookoff point for each aircraft
        for aircraft in formation:
            
            hub_to_destination = aircraft.route.segments[0]
            
            theta = abs(hub_to_destination.get_initial_bearing() -
                        trunk_segment.get_initial_bearing())
            (a, b) = project_segment(theta, hub_to_destination.get_length())
            Q = get_hookoff_quotient(a, b, config.alpha)
            
            hookoff_point = formation.hub.get_position(
                trunk_segment.get_initial_bearing(),
                a * Q
            )
            
            aircraft.route.waypoints = [hookoff_point] +\
                                        aircraft.route.waypoints

            aircraft.route.init_segments()
            aircraft.controller.calibrate()
