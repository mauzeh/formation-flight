from pydispatch import dispatcher
from geo.waypoint import Waypoint

def register():
    dispatcher.connect(handle)

def handle(signal, sender, data = None, time = 0):

    if not hasattr(handle, "assigner"):
        handle.assigner = Assigner()

    #if signal is 'fly':
        #print 'flyyyyyyyyyyyy!'
        #handle.assigner.lock_formations(signal, sender, data, time)
    if signal is 'takeoff':
        print 'taaaaaaaaaake off'
        handle.assigner.assign(flight = sender)
        
class Assigner(object):
    """Assigns flights to a virtual hub"""

    def assign(self, flight):
        print 'finding a virtual hub for %s' % flight
        hub = Waypoint('AMS')
        print hub
        # replace the direct route with a route via the virtual hub
        waypoints = flight.route.