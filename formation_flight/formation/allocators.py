"""Allocators determine which flights should be bundled in a formation."""

from lib.intervals import Interval, group
from lib import sim, debug
from lib.debug import print_line as p
from models import Formation
import config

class FormationAllocator(object):
    """Generic allocation: no filter."""
    
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

    def add_aircraft(self, aircraft):
        self.aircraft_queue.append(aircraft)

    def remove_aircraft(self, aircraft):
        self.aircraft_queue.remove(aircraft)

class FormationAllocatorEtah(FormationAllocator):
    """Uses interval overlapping to group aircraft into formations"""
    
    def allocate(self, aircraft):

        self.formations = []
        intervals       = []
        candidates      = self.aircraft_queue
        hub             = aircraft.route.waypoints[0]

        # This is bad. We don't want to filter anything. 
        # @todo: pre-process at a higher level.
        candidates = filter(lambda a: a.route.waypoints[0] is hub, 
                            self.aircraft_queue)

        for candidate in candidates:

            # Quick and dirty: recalc position. Instead, pull eta from var.
            candidate.controller.update_position()
            hub_eta = sim.time + candidate.time_to_waypoint()
            p('Hub eta %s for candidate %s' % (hub_eta, candidate))
            intervals.append(Interval(
                candidate,
                hub_eta - config.etah_slack,
                hub_eta + config.etah_slack
            ))
        for interval_group in group(intervals):
            formation = Formation()
            for interval in interval_group:
                formation.append(interval.obj)
            self.formations.append(formation)
