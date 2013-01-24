"""Implementation of hook-off model."""
import math
import config
from lib.geo.point import Point
from lib.geo.waypoint import Waypoint
from lib.geo.segment import Segment

# Weight of aircraft when reaching the hub
W_hub = 260000

def omega(W_1, d):
    V = 500
    c_T = .6
    L_D = 19
    return W_1 * (1-math.exp(-d*c_T/(V*L_D)))

def d(p1, p2):
    return p1.distance_to(p2)
    pass

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

# How far into the trunk route are we staying in the formation?
hookoff_distance = trunk.get_length()

fuel_total = 99999999999999999

while hookoff_distance > 0:

    # Where is our hookoff then located?
    hookoff = hub.get_position(
        trunk.get_initial_bearing(),
        hookoff_distance
    )
    
    # Set the next iteration value
    hookoff_distance -= 15    
    
    # If hookoff too close to dest, then skip this iteration
    if(d(hookoff, des) < 150):
        continue

    # Fuel burn over formation segment
    F_3 = (1-alpha) * omega(W_hub, d(hub, hookoff))

    # Fuel burn over solo segment from hub to TOD)
    F_4 = omega(W_hub - F_3, d(hookoff, des)-150)

    # Stop the loop if we have surpassed our optimum
    # Also rewind the hookoff point by one step
    if F_3 + F_4 > fuel_total:
        hookoff_distance += 30
        hookoff = hub.get_position(
            trunk.get_initial_bearing(),
            hookoff_distance
        )
        break

    print fuel_total
    fuel_total = F_3 + F_4

print 'The trunk length = %d NM' % trunk.get_length()
print 'The hookoff distance = %d NM' % d(hub, hookoff)
print 'Therefore, Q = %.2f' % (d(hub, hookoff) / trunk.get_length())

def run():
    print 'haha'