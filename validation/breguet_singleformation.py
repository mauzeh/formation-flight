import math
import lib.sim
from lib.debug import print_dictionary
from lib.geo.util import formationburn
from lib.geo.util import get_weight_ratio
from lib.debug import print_line as p

from lib.geo.waypoint import Waypoint
from lib.geo.point import Point
from lib.geo.route import Route

import copy

import numpy as np
import matplotlib.pyplot as plt

def w(d, W, model):
    result = W * (1 - math.exp(-d * model['c_T'] / (model['V'] * model['L_D'])))
    p('validate', 'Calculating fuel burned.')
    p('validate', 'Distance: %.2f' % d)
    p('validate', 'Starting weight: %.2f' % W)
    p('validate', 'Result: %d' % result)
    p('validate', '===========================')
    return result

def fuel_per_stage(d_1, d_2, model, discount = 0):

    taxi_fuel   = 500
    F_0         = 8026 + taxi_fuel
    F_1         = w(d_1, model['MTOW'] - F_0, model)
    
    F_2         = (1 - discount) * w(d_2, model['MTOW'] - F_0 - F_1, model)
    F_3         = 0
    F_4         = 385 + taxi_fuel
    return [F_0, F_1, F_2, F_3, F_4]

def execute():

    models = {
        '777'  : {
            'V'    : 500,
            'c_T'  : .56,
            'L_D'  : 19.26,
            'MTOW' : 300000
        },
        '767'  : {
            'V'    : 500,
            'c_T'  : .54,
            'L_D'  : 17,
            'MTOW' : 190000
        },
        '330'  : {
            'V'    : 500,
            'c_T'  : .54,
            'L_D'  : 17,
            'MTOW' : 190000
        },
        '340'  : {
            'V'    : 500,
            'c_T'  : .54,
            'L_D'  : 17,
            'MTOW' : 250000
        }
    }

    # Temporary
    hub = Waypoint('MAN')

    formation = [{
        'aircraft' : '777',
        'route'    : Route([Waypoint('DUS'), Waypoint('IAD')]),
        'discount' : 0,
    },{
        'aircraft' : '767',
        'route'    : Route([Waypoint('BRU'), Waypoint('ORD')]),
        'discount' : 0.13
    },{
        'aircraft' : '330',
        'route'    : Route([Waypoint('AMS'), Waypoint('IAH')]),
        'discount' : 0.13
    }]

    solo = [{
        'aircraft' : '767',
        'route'    : Route([Waypoint('LHR'), Waypoint('ATL')])
    },{
        'aircraft' : '340',
        'route'    : Route([Waypoint('FRA'), Waypoint('SFO')])
    }]
    
    benchmark = copy.deepcopy(formation) + copy.deepcopy(solo)

    # Origin to TOC
    d_0 = 100
    
    # Exit to TOC
    d_3 = 0

    # TOD to Destination
    d_4 = 150

    F_formation = 0
    for flight in formation:

        # Direct great circle connection
        d_direct = flight['route'].get_length()
        
        # Distance from origin to hub
        origin_to_hub   = Route([flight['route'].waypoints[0], hub])
        d_origin_to_hub = origin_to_hub.get_length()
        
        # TOC to hub
        d_1 = d_origin_to_hub - d_0
        
        # Hub to exit
        d_2 = d_direct - d_0 - d_1 - d_3 - d_4
        
        flight['f'] = fuel_per_stage(
            d_1, d_2, models[flight['aircraft']], flight['discount']
        )
        flight['d'] = [d_0, d_1, d_2, d_3, d_4]

        F_formation += sum(flight['f'])

    print 'formation fuel burn: %.2f' % (F_formation)

    F_solo = 0
    for flight in solo:

        # Direct great circle connection
        d_direct = flight['route'].get_length()

        # Distance from origin to hub
        origin_to_hub   = Route([flight['route'].waypoints[0], hub])
        d_origin_to_hub = origin_to_hub.get_length()

        # TOC to hub
        d_1 = d_origin_to_hub - d_0

        # Hub to TOD (not to exit point)
        d_2 = d_direct - d_0 - d_1 - d_4
        
        flight['f'] = fuel_per_stage(
            d_1, d_2, models[flight['aircraft']]
        )
        flight['d'] = [d_0, d_1, d_2, d_3, d_4]
        
        F_solo += sum(flight['f'])

    print 'solo fuel burn: %.2f' % (F_solo)

    F_b = 0
    for flight in benchmark:

        # In the benchmark scenario, fly directly from origin to destination
        d_1 = flight['route'].get_length() - d_0 - d_4
        d_2 = 0

        flight['f'] = fuel_per_stage(
            d_1, d_2, models[flight['aircraft']]
        )
        flight['d'] = [d_0, d_1, d_2, d_3, d_4]
        
        F_b += sum(flight['f'])

    print 'benchmark fuel burn: %.2f' % (F_b)

    F_s = 100 * (F_b - (F_formation + F_solo)) / F_b
    print 'fuel saved: %.2f%%' % F_s
    
    print '--DISTANCE: formation flying scenario--'
    for i in [0,1,2,3,4]:
        row = r'$d_i^%d$' % i
        for flight in formation + solo:
            row += ' & %d' % flight['d'][i]
        row += r' \\'
        print row
    print r'\hline'
    row = r'$\sum$'
    for flight in formation + solo:
        row += ' & %d' % sum(flight['d'])
    row += r' \\'
    print row
    
    print '--DISTANCE: benchmark scenario--'
    for i in [0,1,2,3,4]:
        row = r'$F_i^%d$' % i
        for flight in benchmark:
            row += ' & %d' % flight['d'][i]
        row += r' \\'
        print row
    print r'\hline'
    row = r'$\sum$'
    for flight in benchmark:
        row += ' & %d' % sum(flight['d'])
    row += r' \\'
    print row

    print '--FUEL: formation flying scenario--'
    for i in [0,1,2,3,4]:
        row = r'$F_i^%d$' % i
        for flight in formation + solo:
            row += ' & %d' % flight['f'][i]
        row += r' \\'
        print row
    print r'\hline'
    row = r'$\sum$'
    for flight in formation + solo:
        row += ' & %d' % sum(flight['f'])
    row += r' \\'
    print row

    print '--FUEL: benchmark scenario--'
    for i in [0,1,2,3,4]:
        row = r'$F_i^%d$' % i
        for flight in benchmark:
            row += ' & %d' % flight['f'][i]
        row += r' \\'
        print row
    print r'\hline'
    row = r'$\sum$'
    for flight in benchmark:
        row += ' & %d' % sum(flight['f'])
    row += r' \\'
    print row













