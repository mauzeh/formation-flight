import math
import numpy as np
import matplotlib.pyplot as plt

def get_range(V, C, L_D, W_1, W_2):
    return (V / C) * L_D * math.log(float(W_1) / W_2)

def get_weight_ratio(V, C, L_D, distance):
    return math.exp(distance * C / (V * L_D))

# Knots
V = 490

# Specific fuel consumption (engine design)
# Taken from http://adg.stanford.edu/aa241/propulsion/largefan.html
C = .60

# L over D (airframe design)
# Taken from http://www.pprune.org/tech-log/319851-lift-drag-ratio-a320.html
L_D = 19.26

# How many kgs one liter of Jet A1 is
fuel_conversion = 0.79

# Maximum fuel capacity (kg)
MaxFuelCapacity = 171176 * fuel_conversion

# Maximum Take Off Weight (kg)
# Taken from http://en.wikipedia.org/wiki/Boeing_777
MTOW = 297550

# How much fuel you are going to burn to reach cruise
# Estimated at around 14 tonnes, includes ground taxi
# Taken from http://www.airliners.net/aviation-forums/tech_ops/read.main/42100
# Another good thread:
# http://www.airliners.net/aviation-forums/tech_ops/read.main/83781/
DepartFuel = 10000 + 13000

# How much fuel you are willing to burn during cruise (kg)
CruiseFuel = MaxFuelCapacity - DepartFuel

# Weight of aircraft at start of cruise (kg)
# Have to deduct fuel burned to reach cruise
W_1 = MTOW - DepartFuel

# Weight of aircraft at end of cruise (kg)
W_2 = W_1 - CruiseFuel

if __name__ == '__main__':

    print 'W_1 / W_2 = %d / %d = %s' % (float(W_1), W_2, float(W_1)/W_2)
    print get_range(V, C, L_D, W_1, W_2)
    
    #fractions = [float(i)/100 for i in range(1, 100)]
    #ranges = [get_range(V, C, L_D, 1, fraction) for fraction in fractions]
    #plt.plot(fractions, ranges)
    #plt.show()