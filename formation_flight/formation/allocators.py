"""Allocators determine which flights should be bundled in a formation."""

from lib.intervals import Interval, group
from lib import sim, debug
from lib.debug import print_line as p
from models import Formation
import config

from lib.geo.segment import Segment

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
        try:
            self.aircraft_queue.remove(aircraft)
        except ValueError:
            p('Could not remove %s from queue because not present' % aircraft)

class FormationAllocatorEtah(FormationAllocator):
    """Uses interval overlapping to group aircraft into formations"""
    
    def allocate(self, aircraft):
        
        p('debug', 'Starting formation allocation for %s' % aircraft)
        
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
        
        p('debug', 'Full candidate set: %s' % candidates)

        # Only consider aircraft having a maximum heading difference between
        # the hub and their destination
        segment = Segment(aircraft.hub, aircraft.destination)
        leader_heading = segment.get_initial_bearing()

        def heading_filter(buddy):

            segment = Segment(buddy.hub, buddy.destination)
            buddy_heading = segment.get_initial_bearing()
            phi_obs = abs(leader_heading - buddy_heading)
            p(
                'debug',
                'delta phi observed for %s (phi: %.2f) against %s (phi: %.2f)'
                ': %.2f degrees' % (
                    aircraft, leader_heading, buddy, buddy_heading, phi_obs
                )
            )
            return phi_obs < config.phi_max

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
        
        p('debug', 'Reduced candidate set: %s' % candidates)

        for candidate in candidates:

            # Quick and dirty: recalc position. Instead, pull eta from var.
            candidate.controller.update_position()
            tth = candidate.time_to_waypoint() # time to hub
            hub_eta = sim.time + tth
            
            # From the moment the aircraft enters the lock area, the slack
            # decreases linearly to zero upon hub arrival.
            if tth < config.lock_time:
                slack = tth * config.etah_slack / config.lock_time
            else:
                slack = config.etah_slack

            p('Time = %s, Hub (= %s) eta %s for candidate %s' %\
              (sim.time, hub, hub_eta, candidate))
            intervals.append(Interval(
                candidate,
                int(hub_eta) - slack,
                int(hub_eta) + slack
            ))
            
        for interval_group in group(intervals):
            formation = Formation()
            for interval in interval_group:
                formation.append(interval.obj)
            self.formations.append(formation)
