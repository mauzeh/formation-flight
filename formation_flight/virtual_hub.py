import random

from pydispatch import dispatcher
from geo.waypoint import Waypoint

# Hubs that can be assigned to flights.
hubs = [Waypoint('MAN')]#, Waypoint('EIN'), Waypoint('AMS')]

def register():
    dispatcher.connect(handle)

def handle(signal, sender, data = None, time = 0):

    if not hasattr(handle, "assigner"):
        handle.assigner = Assigner()

    if signal is 'takeoff':
        handle.assigner.assign(flight = sender)
        
class Assigner(object):
    """Assigns flights to a virtual hub"""

    def assign(self, flight):

        # find an appropriate hub for this flight
        hub = random.choice(hubs)
        #print 'flight %s is getting hub %s' % (flight, hub)

        # replace the direct route with a route via the virtual hub
        waypoints = flight.route.waypoints
        new_waypoints = waypoints[:1] + [hub] + waypoints[1:]
        flight.route.waypoints = new_waypoints
        flight.route.init_segments()