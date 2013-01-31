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
    
    model = {
        'name' : 'B772',
        'W_1'  : W_1,
        'V'    : 500,
        'c_L'  : .6,
        'L_D'  : 19.26
    }
    
    # Split the segment hub-destination up into a trunk segment and a
    # cross segment
    (trunk, cross) = project_segment(trunk_deviation, hub_to_destination)
    
    for alpha in np.arange(.04, .20, .02):

        (Q_list, Q_opt, fuel_list, fuel_opt) =\
            get_hookoff(alpha, trunk, cross, model)

        plt.plot(Q_list, fuel_list, label = r'$\alpha=%s$' % alpha)
        plt.plot(Q_opt, fuel_opt, 'sb')
    
    plt.xlabel('Q', fontweight = 'bold')
    plt.ylabel('Fuel Burn', fontweight = 'bold')
    plt.legend(loc=(0.05, 0.05))
    plt.title('Breguet Fuel Burn Against Q (B777-200ER)', fontsize = 16, fontweight = 'bold')
    plt.show()
    
    #x = []
    #y = []
    #for alpha in np.arange(0, 1, .005):
    #    (Q_list, Q_opt, fuel_list, fuel_opt) = get_hookoff(alpha, trunk, cross, W_1)
    #    x.append(alpha)
    #    y.append(Q_opt)
    #
    #plt.plot(x, y, )
    #plt.xlabel('Q')
    #plt.ylabel('Fuel Burn')
    #plt.legend(loc=(0.05, 0.05))
    #plt.title(
    #    r'$Q_{opt}$ against $\alpha$ using Breguet Fuel Estimation (B777-200ER)'
    #)
    #plt.show()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    