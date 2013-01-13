"""Handlers listen and react to events."""

from controllers import AircraftController
from lib import sim
from lib.debug import print_line as p

def init():
    sim.dispatcher.register('aircraft-init', handle_init)
    sim.dispatcher.register('aircraft-depart', handle_departure)
    sim.dispatcher.register('aircraft-at-waypoint', handle_waypoint)
    sim.dispatcher.register('aircraft-arrive', handle_arrival)

def handle_init(event):
    aircraft = event.sender
    aircraft.controller = AircraftController(aircraft)
    aircraft.controller.schedule_departure()

def handle_departure(event):
    aircraft = event.sender
    aircraft.depart()
    aircraft.controller.calibrate()

def handle_waypoint(event):
    aircraft = event.sender
    aircraft.at_waypoint()
    p('Aircraft at waypoint: %s (%s)' % (
        aircraft.position,
        aircraft
    ))
    p('Need to calibrate aircraft %s (%s)' % (
        aircraft, aircraft.route
    ))
    aircraft.controller.calibrate()

def handle_arrival(event):
    aircraft = event.sender
    aircraft.arrive()
