import math
import lib.sim
from lib.debug import print_dictionary
from lib.geo.util import formationburn
from lib.geo.util import get_weight_ratio
from lib.debug import print_line as p

from lib.geo.waypoint import Waypoint
from lib.geo.point import Point
from lib.geo.segment import Segment
from lib.geo.route import Route

from lib.geo.util import project_segment, get_hookoff_quotient, midpoint

import copy
import config

import numpy as np
import matplotlib.pyplot as plt

config.Z = .25#0.065

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

def get_hub(flights):
    o = []
    d = []
    for flight in flights:
        o.append(flight['route'].waypoints[0])
        d.append(flight['route'].waypoints[-1])
    mid_o = midpoint(o)
    mid_d = midpoint(d)
    trunk_route = Segment(mid_o, mid_d)
    return mid_o.get_position(
        trunk_route.get_initial_bearing(),
        trunk_route.get_length() * config.Z
    )
    
def get_trunk_route(hub, formation):
    destinations = []
    for aircraft in formation:
        destinations.append(aircraft['route'].waypoints[-1])
    mid_d = midpoint(destinations)
    return Segment(hub, mid_d)

def get_exit(hub, trunk_route, flight):
    dest = flight['route'].waypoints[-1]
    hub_to_dest = Segment(hub, dest)
    theta = abs(hub_to_dest.get_initial_bearing() -
                trunk_route.get_initial_bearing())
    (a, b) = project_segment(theta, hub_to_dest.get_length())
    Q = get_hookoff_quotient(a, b, config.alpha)
    d_hub_to_exit = a * Q
    
    # Exit to destination must be long enough to allow for safe descent
    # TOD is at 150NM out of dest, so exit->dest must be longer than 150NM
    d_exit_to_dest = 0
    while d_exit_to_dest < 150:
        exit_point = hub.get_position(
            trunk_route.get_initial_bearing(),
            d_hub_to_exit
        )
        d_hub_to_exit -= 1
        exit_dest = Segment(exit_point, dest)
        d_exit_to_dest = exit_dest.get_length()
    assert exit_dest.get_length() > 150
    print 'For flight %s, the exit point is %dNM away from dest' % (
        flight['route'], d_exit_to_dest
    )
    return exit_point
    
def execute():

    models = {
        '777'  : {
            'V'    : 500,
            'c_T'  : .56,
            'L_D'  : 19.26,
            'MTOW' : 200000
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

    formation = [{
        'aircraft' : '777',
        'route'    : Route([Waypoint('DUS'), Waypoint('IAD')]),
        'discount' : 0,
    },{
        'aircraft' : '777',
        'route'    : Route([Waypoint('BRU'), Waypoint('ORD')]),
        'discount' : config.alpha
    },{
        'aircraft' : '777',
        'route'    : Route([Waypoint('AMS'), Waypoint('IAH')]),
        'discount' : config.alpha
    }]

    solo = [{
        'aircraft' : '777',
        'route'    : Route([Waypoint('LHR'), Waypoint('ATL')])
    },{
        'aircraft' : '777',
        'route'    : Route([Waypoint('FRA'), Waypoint('SFO')])
    }]
    
    hub = get_hub(formation + solo)
    
    benchmark = copy.deepcopy(formation) + copy.deepcopy(solo)
    
    trunk_route = get_trunk_route(hub, formation)
    print trunk_route

    # Origin to TOC
    d_0 = 100
    
    # Exit to TOD
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
        exit_point = get_exit(hub, trunk_route, flight)
        hub_to_exit = Segment(hub, exit_point)
        d_2 = hub_to_exit.get_length()
        
        # Exit to TOD
        exit_to_dest = Segment(exit_point, flight['route'].waypoints[-1])
        d_3 = exit_to_dest.get_length() - d_4
        
        flight['f'] = fuel_per_stage(
            d_1, d_2, models[flight['aircraft']], flight['discount']
        )
        flight['d'] = [d_0, d_1, d_2, d_3, d_4]

        F_formation += sum(flight['f'])

    print 'formation fuel burn: %.2f' % (F_formation)
    
    # Origin to TOC
    d_0 = 100
    
    # Exit to TOD
    d_3 = 0

    # TOD to Destination
    d_4 = 150

    F_solo = 0
    for flight in solo:

        # Total route length
        full_route = Route([
            flight['route'].waypoints[0],
            hub,
            flight['route'].waypoints[-1],
        ])
        d_total = full_route.get_length()

        # Distance from origin to hub
        origin_to_hub   = Route([flight['route'].waypoints[0], hub])
        d_origin_to_hub = origin_to_hub.get_length()

        # TOC to hub
        d_1 = d_origin_to_hub - d_0

        # Hub to TOD (not to exit point)
        d_2 = d_total - d_0 - d_1 - d_4

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

#def temp():

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
    
    S_d = (
        formation[0]['d'][2] +\
        formation[1]['d'][2] +\
        formation[2]['d'][2]
    )/(
        sum(formation[0]['d']) +\
        sum(formation[1]['d']) +\
        sum(formation[2]['d']) +\
        sum(solo[0]['d']) +\
        sum(solo[1]['d'])
    )
    
    F_s = 1 - (
        sum(formation[0]['f']) +\
        sum(formation[1]['f']) +\
        sum(formation[2]['f']) +\
        sum(solo[0]['f']) +\
        sum(solo[1]['f'])
    )/(
        sum(benchmark[0]['f']) +\
        sum(benchmark[1]['f']) +\
        sum(benchmark[2]['f']) +\
        sum(benchmark[3]['f']) +\
        sum(benchmark[4]['f'])
    )
    
    p_tot = (
        sum(formation[0]['d']) +\
        sum(formation[1]['d']) +\
        sum(formation[2]['d']) +\
        sum(solo[0]['d']) +\
        sum(solo[1]['d'])
    )/(
        sum(benchmark[0]['d']) +\
        sum(benchmark[1]['d']) +\
        sum(benchmark[2]['d']) +\
        sum(benchmark[3]['d']) +\
        sum(benchmark[4]['d'])
    ) - 1

    print '--ANALYTICAL OUTPUT RESULTS--'
    print r'$S_f$ & 0.6 & 0.6 \\'
    print r'$S_d$ & %.4f & %.4f \\' % (S_d, S_d)
    print r'$F_s$ & FILLIN & FILLIN \\'
    print r'$F^{rel}_s$ & %.4f & %.4f \\' % (F_s, F_s)
    print r'$p_{tot}$ & %.4f & %.4f \\' % (p_tot, p_tot)
    











