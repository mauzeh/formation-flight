import math
import lib.sim
from lib.debug import print_dictionary
from lib.geo.util import get_fuel_burned_during_cruise
from lib.geo.util import formationburn
from lib.geo.util import get_weight_ratio
from lib.debug import print_line as p

import copy

import numpy as np
import matplotlib.pyplot as plt

model = {
    'name' : 'B772',
    'V'    : 500,
    'c_L'  : .6,
    'L_D'  : 17,
    'W_1'  : 300000
}

vars = {}

vars['formation_size']         = 6
vars['origin_to_hub']          = 242
vars['origin_to_destination']  = 3193
vars['hookoff_to_destination'] = 0

vars['hub_to_hookoff']         = (
    vars['origin_to_destination'] -
    vars['origin_to_hub'] -
    vars['hookoff_to_destination']
)

vars['fuel_benchmark']         = 0
vars['fuel_formation']         = 0

p('validate', 'Getting the benchmark fuel')
vars['fuel_benchmark'] = vars['formation_size'] *\
    get_fuel_burned_during_cruise(vars['origin_to_destination'], model)
p('validate', 'OK, we have the benchmark fuel now')

incurs_benefit = False

for i in range(0, vars['formation_size']):
    
    model = copy.deepcopy(model)

    if incurs_benefit is True:
        discount = .13
    else:
        discount = 0
    
    vars['fuel_formation'] += (
        formationburn(
            vars['origin_to_hub'],
            vars['hub_to_hookoff'],
            vars['hookoff_to_destination'],
            model, discount
        )
    )

    incurs_benefit = True

vars['fuel_saved'] = vars['fuel_benchmark'] - vars['fuel_formation']
vars['fuel_saved_rel'] = (
    vars['fuel_saved'] / vars['fuel_benchmark']
)

print_dictionary(vars)
































