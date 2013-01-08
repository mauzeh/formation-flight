import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline

from lib.geo.util import get_range
from lib.geo.util import get_weight_ratio
from lib.geo.util import project_segment
from lib.geo.util import get_hookoff

def run():

    alpha              = .13 # Formation discount
    hub_to_destination = 1500 # distance in NM
    trunk_deviation    = 4 # degrees
    W_1                = 297550 - 14000 # B777 Maxweight at start of cruise

    font = {'family' : 'sans-serif',
            'weight' : 'normal',
            'size'   : 12}

    models = [{
        'name' : 'B772',
        'W_1'  : W_1,
        'V'    : 500,
        'c_L'  : .6,
        'L_D'  : 19.26
    },{
        'name' : 'A333',
        'W_1'  : W_1,
        'V'    : 500,
        'c_L'  : .5,
        'L_D'  : 17
    },{
        'name' : 'B763',
        'W_1'  : W_1,
        'V'    : 500,
        'c_L'  : .48,
        'L_D'  : 16
    }]

    matplotlib.rc('font', **font)
    matplotlib.rc('mathtext', default='sf')

    # Split the segment hub-destination up into a trunk segment and a
    # cross segment
    (trunk, cross) = project_segment(trunk_deviation, hub_to_destination)

    for model in models:
    
        x = []
        y = []
        for alpha in np.arange(0.10, .16, .005):
            
            (Q_list, Q_opt, fuel_list, fuel_opt) =\
            get_hookoff(alpha, trunk, cross, model)
            
            x.append(alpha)
            y.append(Q_opt)
        
        plt.plot(x, y, label = model['name'])
        plt.legend(loc=(0.05, 0.05))
        plt.xlabel(r'$\alpha$')
        plt.ylabel(r'$Q$')
        plt.title(
            r'$Q_{opt}$ against $\alpha$ using Breguet Fuel Estimation'
        )
    plt.show()