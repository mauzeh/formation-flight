"""
Find the location of the starting point on a discounted trajectory.

Assumptions:
1 - One aircraft, 2D plane.
2 - One discounted trajectory.
3 - Point of departure does not reside on discounted trajectory.
"""

import math
from sympy import Symbol

if __name__ == "__main__":
    a       = 1
    alpha   = 15
    beta_h  = 1.5
    beta_f  = 1 

    alpha   = math.radians(alpha)

    def tiny(x): return float(x)/100

    for Q in map(tiny, range(0, 101)):

        h       = a * math.sqrt(1 + pow(Q / math.cos(alpha),2) - 2*Q)
        f       = Q * a / math.cos(alpha)
        k_total = beta_h * h + beta_f * f

        print "%f %f" % (Q, k_total)
