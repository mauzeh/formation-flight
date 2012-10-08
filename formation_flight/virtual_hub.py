import random

from aircraft import Aircraft
from lib.geo.waypoint import Waypoint
import simulator, config

hubs = []
for hub_name in config.hubs:
    hubs.append(Waypoint(hub_name))

def register():
    print 'still need to connect virtual_hub to events'
    #dispatcher.connect(handle)

def handle(signal, sender, data = None, time = 0):

    if not hasattr(handle, "assigner"):
        handle.assigner = Assigner()

    if signal is 'takeoff':
        handle.assigner.assign(aircraft = sender)
        
class Assigner(object):
    """Assigns flights to a virtual hub"""

    def assign(self, aircraft):

        assert type(aircraft) is Aircraft

        # find an appropriate hub for this flight
        hub = random.choice(hubs)
        #print 'aircraft %s (dep: %d, starttime: %d) is getting hub %s' %\
               #(aircraft, aircraft.departure_time,simulator.starttime, hub)

        # replace the direct route with a route via the virtual hub
        waypoints = aircraft.route.waypoints
        new_waypoints = waypoints[:1] + [hub] + waypoints[1:]
        aircraft.route.waypoints = new_waypoints
        aircraft.route.init_segments()
