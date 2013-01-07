"""Allocators determine which flights should be bundled in a formation."""

from lib.intervals import Interval, group
from lib import sim, debug
from lib.debug import print_line as p
from models import Formation
import config

class FormationAllocator(object):
    """Abstract Allocator. Creates one giant formation."""
    
    def __init__(self):
        self.aircraft_queue = []
        self.formations = []

    def allocate(self, aircraft):
        # No filtering, put all aircraft in one big formation.
        self.formations = [self.aircraft_queue]

    def find_formation(self, aircraft):
        self.allocate(aircraft)
        """Finds the formation having the aircraft requested"""
        for formation in self.formations:
            if aircraft in formation:
                return formation
        raise Exception("No formation having %s found" % aircraft)

    def add_aircraft(self, aircraft):
        self.aircraft_queue.append(aircraft)

    def remove_aircraft(self, aircraft):
        self.aircraft_queue.remove(aircraft)

class FormationAllocatorEtah(FormationAllocator):
    """Uses interval overlapping to group aircraft into formations"""
    
    def allocate(self, aircraft):
        
        # Do not perform allocation if no hub exists in the flight route.
        if len(aircraft.route.segments) == 0:
            return

        self.formations = []
        intervals       = []
        candidates      = self.aircraft_queue
        hub             = aircraft.route.waypoints[0]

        # This is bad. We don't want to filter anything. 
        # @todo: pre-process at a higher level.
        # Only consider other aircraft flying to the same hub
        candidates = filter(lambda a: a.route.waypoints[0] is hub, 
                            candidates)

        # Only consider aircraft having a maximum heading difference between
        # the hub and their destination
        leader_heading = aircraft.route.segments[0].get_initial_bearing()
        def heading_filter(buddy):
            buddy_heading = buddy.route.segments[0].get_initial_bearing()
            return abs(leader_heading - buddy_heading) < config.phi_max
        candidates = filter(heading_filter, candidates)

        # Other interesting filters
        if 'same-airline' in config.restrictions:
            airline = aircraft.label[0:2]
            candidates = filter(lambda a: a.label[0:2] == airline,
                                candidates)
        if 'same-aircraft-type' in config.restrictions:
            aircraft_type = aircraft.aircraft_type
            candidates = filter(lambda a: a.aircraft_type == aircraft_type,
                                candidates)
            
        for candidate in candidates:

            # Quick and dirty: recalc position. Instead, pull eta from var.
            candidate.controller.update_position()
            hub_eta = sim.time + candidate.time_to_waypoint()

            p('Time = %s, Hub (= %s) eta %s for candidate %s' %\
              (sim.time, hub, hub_eta, candidate))
            intervals.append(Interval(
                candidate,
                int(hub_eta) - config.etah_slack,
                int(hub_eta) + config.etah_slack
            ))
            
        for interval_group in group(intervals):
            formation = Formation()
            for interval in interval_group:
                formation.append(interval.obj)
            self.formations.append(formation)
