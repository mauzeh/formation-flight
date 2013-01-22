import math
import lib.sim
from lib.debug import print_dictionary
from lib.geo.util import get_fuel_burned_during_cruise
from lib.geo.util import formationburn
from lib.geo.util import get_weight_ratio

import numpy as np
import matplotlib.pyplot as plt

# B777 MTWO minus some additional measure to account for the fuel burned during
# take-off.
W_1 = 297550 - 14000

model = {
    'name' : 'B772',
    'V'    : 500,
    'c_L'  : .6,
    'L_D'  : 17,
    'W_1'  : W_1
}

x = range(1, 11)
y1 = []
y2 = []

for j in x:

    vars = {}

    vars['formation_size']         = j
    vars['origin_to_destination']  = 3000
    vars['origin_to_hub']          = 150
    vars['hookoff_to_destination'] = 250

    vars['hub_to_hookoff']         = (
        vars['origin_to_destination'] -
        vars['origin_to_hub'] -
        vars['hookoff_to_destination']
    )
    
    vars['fuel_benchmark']         = 0
    vars['fuel_formation']         = 0

    model['W_1'] = W_1
    vars['fuel_benchmark'] = vars['formation_size'] *\
        get_fuel_burned_during_cruise(vars['origin_to_destination'], model)

    incurs_benefit = False
    
    for i in range(0, vars['formation_size']):

        model['W_1'] = W_1
    
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
    
    y1.append(vars['fuel_saved_rel'])
    y2.append((j-1) * .13 / j)
    
    print_dictionary(vars)

print r'$n$ & $F_{s, max}$ & $\alpha_{max}$ \\'

for i in x:
    
    print r'%d & %.1f\%% & %.1f\%% \\' % (
        i,
        100 * y1[i-1],
        100 * y2[i-1]
    )

plt.plot(x, y2, label = r'Maximum Discount $\alpha_{max}$')
plt.plot(x, y1, label = r'Maximum Fuel Savings $F_{s,max}$')

plt.title('Upper limits on formation benefits')

plt.xlabel(r'Formation size $N$')
plt.ylabel(r'Benefit')

plt.yticks([
    0,.01,.02,.03,.04,.05,.06,.07,.08,.09,.1,.11,.12,.13
],[
    '0%', '1%', '2%', '3%', '4%', '5%', '6%', '7%', '8%', '9%', '10%', '11%',
    '12%', '13%'
])

plt.ylim([0, .13])
plt.xlim(1, len(x))
plt.xticks(x)
plt.legend(loc = 'lower right')

plt.show()






































