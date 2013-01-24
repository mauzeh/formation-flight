import config
import math
from lib.geo.point import Point
from lib.geo.waypoint import Waypoint
from lib.geo.segment import Segment

def omega(d, W_1):
    V = config.model['V']
    c_T = config.model['c_T']
    L_D = config.model['L_D']
    return W_1 * (1-math.exp(-d*c_T/(V*L_D)))

def d(p1, p2):
    return p1.distance_to(p2)
    pass

def get_hookoff(trunk, des, alpha):

    hub = trunk.start
    mid = trunk.end
    
    W_hub = 1
    
    # How far into the trunk route are we staying in the formation?
    hookoff_distance = trunk.get_length()
    
    fuel_total = 99999999
    
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
            return hookoff
        fuel_total = F_3 + F_4
    
    # If no good location was found, return the hub itself. The aircraft would
    # then hook off rightt away
    return hub