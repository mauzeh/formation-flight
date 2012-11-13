"""Handlers listen and react to events."""

from lib import sim
from allocators import * 
from synchronizers import * 
from lib.debug import print_line as p
from lib.geo.waypoint import Waypoint
from lib.geo.segment import Segment
from lib.geo.util import project_segment, get_hookoff_quotient, midpoint
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
        
        formation = event.sender

        # Determine formation trunk route
        destinations = []
        for aircraft in formation:
            destinations.append(aircraft.route.waypoints[-1])
        arrival_midpoint = midpoint(destinations)
        p('destinations: %s' % destinations)
        p('midpoint = %s' % arrival_midpoint)
        hub_to_midpoint = Segment(formation.hub, arrival_midpoint)

        # Determine hookoff point for each aircraft, except the last
        for aircraft in formation:
            
            hub_to_destination = aircraft.route.segments[0]
            
            theta = abs(hub_to_destination.get_initial_bearing() -
                        hub_to_midpoint.get_initial_bearing())
            (a, b) = project_segment(theta, hub_to_destination.get_length())
            aircraft.Q = get_hookoff_quotient(a, b, config.alpha)
            
            aircraft.hookoff_point = formation.hub.get_position(
                hub_to_midpoint.get_initial_bearing(),
                a * aircraft.Q
            )
            
            hub_to_hookoff = Segment(formation.hub, aircraft.hookoff_point)
            aircraft.P = hub_to_hookoff.get_length() / hub_to_midpoint.get_length()

        # Place aircraft in order, ascending with Q, to fulfill LIFO condition.
        formation = sorted(formation, key = lambda item: item.P)
        
        # The last aircraft: same hookoff point as its remaining buddy.
        formation[-1].Q = formation[-2].Q
        formation[-1].P = formation[-2].P
        formation[-1].hookoff_point = formation[-2].hookoff_point

        for aircraft in formation:
            debug.print_object(aircraft)
            aircraft.route.waypoints = [aircraft.hookoff_point] +\
                                        aircraft.route.waypoints
            aircraft.route.init_segments()
            aircraft.controller.calibrate()
            
            
            
            
            
            
            
            
            
            