from lib.intervals import Interval, group
from lib import sim, debug
from lib.debug import print_line as p
from models import Formation
import config

class FormationAllocator(object):
    
    def __init__(self):
        self.aircraft_queue = []
        self.formations = []

    def assign(self):
        # Put all aircraft in one big formation for now.
        self.formations = []
        formation = Formation()
        for aircraft in self.aircraft_queue:
            formation.append(aircraft)
        self.formations.append(formation)

    def add_aircraft(self, aircraft):
        self.aircraft_queue.append(aircraft)

    def remove_aircraft(self, aircraft):
        self.aircraft_queue.remove(aircraft)

class FormationAllocatorEtah(FormationAllocator):
    
    def assign(self):
        self.formations = []
        intervals = []
        for aircraft in self.aircraft_queue:
            # Quick and dirty: recalc position. Instead, pull eta from var.
            aircraft.controller.update_position()
            hub_eta = sim.time + aircraft.time_to_waypoint()
            p('hub eta %s for aircraft %s' % (hub_eta, aircraft))
            intervals.append(Interval(
                aircraft,
                hub_eta - config.etah_slack,
                hub_eta + config.etah_slack
            ))
        for interval_group in group(intervals):
            formation = Formation()
            for interval in interval_group:
                formation.append(interval.obj)
            self.formations.append(formation)
