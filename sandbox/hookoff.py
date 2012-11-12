import math

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

def get_hookoff_alpha(a, b, beta):
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
    alpha_list = range(0, 90, 5)
    
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

def run():

    print get_hookoff_alpha(1000, 100, .13)
    
    from lib.geo.point import Point

    
    