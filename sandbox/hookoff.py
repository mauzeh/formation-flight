"""Implementation of hook-off model."""
import math
import config
from lib.geo.point import Point
from lib.geo.waypoint import Waypoint
from lib.geo.segment import Segment
from lib.geo.hookoff import d, omega, get_hookoff

def run():
    
    # Discount incurred on formation trajectory by follower
    alpha = .15
    
    # The formation hub
    hub = Waypoint('AMS')
    
    # The end point of trunk route (midpoint of the destinations)
    mid = Waypoint('JFK')
    
    # The actual destination of current participant
    des = Waypoint('SFO')
    
    # The trunk route itself
    trunk = Segment(hub, mid)
    
    hookoff = get_hookoff(trunk, des, alpha)
    
    print 'The trunk length = %d NM' % trunk.get_length()
    print 'The hookoff distance = %d NM' % d(hub, hookoff)
    print 'Therefore, Q = %.2f' % (d(hub, hookoff) / trunk.get_length())