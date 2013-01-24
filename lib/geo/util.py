import math
from point import Point

import numpy as np
from scipy.interpolate import spline
import copy

from ..debug import print_line as p

def get_range(V, C, L_D, W_1, W_2):
    return (V / C) * L_D * math.log(float(W_1) / W_2)

def get_weight_ratio(V, C, L_D, distance):
    answer = math.exp(distance * C / (V * L_D))
    p('validate', 'get weight ratio (V, C, L_D, d) = (%s, %s, %s, %s) = %s' % (
        V, C, L_D, distance, answer
    ))
    return answer

def get_fuel_burned_during_cruise(distance, model = None):
    
    if model is None:
        model = copy.deepcopy(config.model)

    W_1 = model['W_1']
    V   = model['V']
    c_L = model['c_L']
    L_D = model['L_D']
    
    answer = W_1 * (1 - 1 / get_weight_ratio(V, c_L, L_D, distance))
    
    p('validate', 'fuel burn during cruise(): W_1 = %s'    % W_1)
    p('validate', 'fuel burn during cruise(): V = %s'      % V)
    p('validate', 'fuel burn during cruise(): c_L = %s'    % c_L)
    p('validate', 'fuel burn during cruise(): L_D = %s'    % L_D)
    p('validate', 'fuel burn during cruise(): answer = %s' % answer)
    
    return answer

def formationburn(
    d_origin_to_hub, d_hub_to_exit, d_exit_to_destination,
    model = None, discount = 0
):
    """If discount > 0, it is assumed to apply to d_hub_to_exit"""
    
    if model is None:
        model = copy.deepcopy(config.model)
    
    p('validate', 'formationburn()')
    p('validate', 'formationburn(): d_origin_to_hub = %d'       % d_origin_to_hub)
    p('validate', 'formationburn(): d_hub_to_exit = %d'         % d_hub_to_exit)
    p('validate', 'formationburn(): d_exit_to_destination = %d' % d_exit_to_destination)
    p('validate', 'formationburn(): model = %s'                 % model)
    p('validate', 'formationburn(): discount = %s'              % discount)

    # We are going to adjust the model, we don't want the original one to
    # be modified though...
    model = copy.deepcopy(model)
    departure_fuel = get_fuel_burned_during_cruise(d_origin_to_hub, model)
    p('validate', ('departure_fuel = %d' % departure_fuel))
    model['W_1'] -= departure_fuel
    enroute_fuel = get_fuel_burned_during_cruise(d_hub_to_exit, model) *\
        (1 - discount)
    p('validate', ('enroute_fuel = %d' % enroute_fuel))
    model['W_1'] -= enroute_fuel
    arrival_fuel = get_fuel_burned_during_cruise(d_exit_to_destination, model)
    p('validate', ('arrival_fuel = %d' % arrival_fuel))
    
    cruiseburn = departure_fuel + enroute_fuel + arrival_fuel
    
    p('validate', 'formationburn(): answer = %s' % cruiseburn)
    
    return cruiseburn

def get_hookoff(alpha, trunk, cross, model):
    
    Q_list     = np.arange(0, 1, .01)
    W_1        = model['W_1']
    fuel_list  = []

    for Q in Q_list:
    
        # The distance from the hub to the hookoff point
        a = Q * trunk
        
        # The distance from the hookoff point to the destination
        b = math.sqrt((trunk-a)**2 + cross**2)
        
        formation_fuel = (1 - alpha) * get_fuel_burned_during_cruise(a, model)
        
        solo_fuel = get_fuel_burned_during_cruise(b, {
            'W_1' : model['W_1'] - formation_fuel,
            'V'   : model['V'],
            'c_L' : model['c_L'],
            'L_D' : model['L_D']
        })
        fuel = formation_fuel + solo_fuel
        
        fuel_list.append(fuel)
    
    fuel_opt = min(fuel_list)
    Q_opt = Q_list[fuel_list.index(fuel_opt)]
    
    return (Q_list, Q_opt, fuel_list, fuel_opt)

def cross_track_distance(d_13, theta_13, theta_12):
    """Calculate distance from great circle path (1 -> 2) to point (3).

    Adapted from http://www.movable-type.co.uk/scripts/latlong.html

    This implementation does not produce a great-circle distance but a mere
    straight-line (through the earth) distance. We don't need anything more
    complicated for our purposes of comparison.

    d_13:     Distance from origin to third point (any distance measure)
    theta_13: Initial bearing from origin to third point (degrees)
    theta_12: Initial bearing from origin to destination (degrees)
    """
    R = 3440
    return math.asin( math.sin (d_13 / R) *\
                      math.sin (math.radians (theta_13 - theta_12))) * R

def midpoint(points):
    """Calculate an average destination based on a planar average (=bad)

    @todo Replace with vectorized version (most accurate solution)
    """
    assert len(points) > 0

    sum_lat = sum((point.weight if hasattr(point, 'weight') else 1) * point.lat for point in points)
    sum_lon = sum((point.weight if hasattr(point, 'weight') else 1) * point.lon for point in points)
    count = sum((point.weight if hasattr(point, 'weight') else 1) for point in points)
    
    return Point(sum_lat / count, sum_lon / count)

def reduce_points(points):
    """Reduces the input list of points to unique points.
    
    Points are given "weights" for each time they appear in the input list."""
    
    # Reset the points from any previous calls
    for point in points:
        try:
            del point.weight
        except AttributeError:
            pass
    
    ret = []
    for point in points:
        for point_other in ret:
            # If the point is already in our return list
            if point_other.coincides(point):
                point.weight = point_other.weight + 1
                
        # Only add our point if no weight was set
        if not hasattr(point, 'weight'):
            point.weight = 1
            ret.append(point)
    return ret

def point_in_points(point, points):
    """Returns True if the point exists/coincides with any point in the list."""
    for p in points:
        if p.coincides(point):
            return True
    return False

def project_segment(theta, c):
    """Given the angle between lines AB and AC, and given a distance c of AC,
    return the distance a of AB and b of BC.
    
      A
      |\
    a | \ c
      |  \
      B---C
        b

    This implementation does not produce a great-circle distance but a mere
    straight-line (through the earth) distance. We don't need anything more
    complicated for our purposes of comparison.

    float theta: Angle between AB and AC (in degrees)
    float c:     Distance AC.
    """
    theta = math.radians(theta)
    return c * math.cos(theta), c * math.sin(theta)

def get_costs(a, b, alpha, beta):
    """Given a triangle ABC (with B being rectangular), return the cost to
       fly in formation from A to B', and solo from B' to C, where B' is a
       point on AB and is uniquely defined by the angle between BC and B'C.
       
       A
       |\
       | \
       |  \
       B'  \
       |    \
       B-----C
       
       float a:     distance from A to B
       float b:     distance from B to C
       float alpha: angle between BC and B'C (in degrees)
       float beta:  discount factor when flying in formation (0 < beta < 1)
    """
    alpha = math.radians(alpha)
    
    # Alpha cannot be larger than the angle between BC and AC.
    alpha_max = math.acos(b / math.sqrt(math.pow(a, 2) + math.pow(b, 2)));
    
    if alpha > alpha_max:
        raise Exception('alpha = %.2f exceeds the allowed value of %.2f' %\
                        (math.degrees(alpha), math.degrees(alpha_max)))
    
    return a - (1-beta)*b*math.tan(alpha) + b/math.cos(alpha)

def get_hookoff_quotient(a, b, beta):
    """Given a triangle AB'C (with B being rectangular), where AB' is a
       formation trajectory, and B'C is a solo trajectory. Find the hookoff
       point that minimizes fuel burn (using the discount factor beta), and
       return the quotient Q = AB' / AB.
       
       For performance, alpha (angle between BC and B'C) has 5 deg increments.
       
       A
       |\
       | \
       |  \
       B'  \
       |    \
       B-----C
       
       float a:     distance from A to B
       float b:     distance from B to C
       float beta:  discount factor when flying in formation (0 < beta < 1)
    """
    alpha_list = range(0, 99, 1)
    
    # Start from back to front for performance reasons
    alpha_list.reverse()

    costs_list = []
    min_cost = None
    min_alpha = 0
    for alpha in alpha_list:
        try:
            costs = get_costs(a, b, float(alpha), beta)
            if min_cost is None:
                min_cost = costs
            elif min_cost > costs:
                min_cost = costs
            else:
                min_alpha = alpha
                break
            #print 'beta =% 5.2f\talpha =% 5.2f\t%.2f' % (beta, alpha, costs)
        # we have reached the maximum allowable angle between BC and B'C
        except Exception:
            break
    return (a - b*math.tan(math.radians(min_alpha))) / a

if __name__ == "__main__":

    print cross_track_distance (34, 237, 187)