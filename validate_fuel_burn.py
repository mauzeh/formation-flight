import math
import lib.sim
from lib.debug import print_dictionary
from lib.geo.util import get_fuel_burned_during_cruise
from lib.geo.util import get_weight_ratio

# B777 MTWO minus some additional measure to account for the fuel burned during
# take-off.
W_1 = 297550 - 14000

model = {
    'name' : 'B772',
    'W_1'  : W_1,
    'V'    : 500,
    'c_L'  : .6,
    'L_D'  : 19.26
}

vars = {}

vars['formation_size']         = 1
vars['origin_to_destination']  = 3187
vars['origin_to_hub']          = 242
vars['hub_to_hookoff']         = 2951
vars['hookoff_to_destination'] = 0

vars['fuel_benchmark'] = vars['formation_size'] *\
    get_fuel_burned_during_cruise(vars['origin_to_destination'], model)

vars['fuel_formation'] = vars['formation_size'] * (
    get_fuel_burned_during_cruise(vars['origin_to_hub'], model) +
    get_fuel_burned_during_cruise(vars['hub_to_hookoff'], model) +
    get_fuel_burned_during_cruise(vars['hookoff_to_destination'], model)
)

vars['fuel_saved'] = vars['fuel_benchmark'] - vars['fuel_formation']

vars['fuel_saved_rel'] = vars['fuel_saved'] / vars['fuel_benchmark']

print_dictionary(vars)

