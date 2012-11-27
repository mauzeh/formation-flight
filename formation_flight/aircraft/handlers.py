"""Handlers listen and react to events."""

from controllers import AircraftController
from lib import sim
from lib.debug import print_line as p

class AircraftHandler(object):

    def __init__(self):
        sim.dispatcher.register('aircraft-init', self.handle_init)
        sim.dispatcher.register('aircraft-depart', self.handle_departure)
        sim.dispatcher.register('aircraft-at-waypoint', self.handle_waypoint)
        sim.dispatcher.register('aircraft-arrive', self.handle_arrival)
        
    def handle_init(self, event):
        aircraft = event.sender
        aircraft.controller = AircraftController(aircraft)
        aircraft.controller.schedule_departure()

    def handle_departure(self, event):
        aircraft = event.sender
        aircraft.depart()
        aircraft.controller.calibrate()

    def handle_waypoint(self, event):
        aircraft = event.sender
        aircraft.at_waypoint()
        p('Need to calibrate aircraft %s (%s)' % (
            aircraft, aircraft.route
        ))
        aircraft.controller.calibrate()

    def handle_arrival(self, event):
        aircraft = event.sender
        aircraft.arrive()
