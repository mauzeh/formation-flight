from controllers import AircraftController
from lib import sim

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
