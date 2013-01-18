import math
import lib.sim
from lib.debug import print_dictionary
from lib.geo.util import formationburn
from lib.geo.util import get_weight_ratio
from lib.debug import print_line as p

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

def sum_F(d_1, d_2, model, discount = 0):
    
    taxi_fuel   = 500
    F_0   = 8026 + taxi_fuel
    F_1   = w(d_1, model['MTOW'] - F_0, model)
    
    F_2   = (1 - discount) * w(d_2, model['MTOW'] - F_0 - F_1, model)
    F_3   = 385 + taxi_fuel
    F     = F_0 + F_1 + F_2 + F_3
    return F

def execute():
    
    models = {
        '772'  : {
            'V'    : 500,
            'c_T'  : .56,
            'L_D'  : 19.26,
            'MTOW' : 300000
        }
    }
    
    # Direct great circle connection
    d_direct = 3157
    
    # Distance from origin to hub
    d_origin_to_hub = 537
    
    # Origin to TOC
    d_0 = 100
    
    # TOD to Destination
    d_3 = 150 

    # TOC to hub
    d_1 = d_origin_to_hub - d_0
    
    # Formation portion of the flight
    d_2 = d_direct - d_0 - d_1 - d_3 # Hub to exit
    
    assert d_1 > 0
    
    F_1 = sum_F(d_1, d_2, models['772'], discount = 0)
    F_2 = sum_F(d_1, d_2, models['772'], discount = .13)
    F_formation = F_1 + F_2
    print 'formation fuel burn: %.2f' % (F_formation)
    
    # In the benchmark scenario, we fly directly from origin to destination
    d_1 = d_direct - d_0 - d_3
    d_2 = 0
    
    F_1 = sum_F(d_1, d_2, models['772'], discount = 0)
    F_2 = F_1
    F_benchmark = F_1 + F_2
    print 'benchmark fuel burn: %.2f' % (F_benchmark)
    
    F_s = 100 * (F_benchmark - F_formation) / F_benchmark
    print 'fuel saved: %.2f%%' % F_s
    









