"""
Find the location of the starting point on a discounted trajectory.

Assumptions:
1 - One aircraft, 2D plane.
2 - One discounted trajectory.
3 - Point of departure does not reside on discounted trajectory.
"""

import math

def get_derivative(a = 1, alpha = 15, beta_h = 1.5, beta_f = 1):

    alpha = math.radians(alpha)

    x = []
    y = []

    accuracy = 0.01

    Qs = map(lambda x: x * accuracy, range(0, int(1 + 1 / accuracy)))

    for Q in Qs:

        h       = a * math.sqrt(1 + pow(Q / math.cos(alpha),2) - 2*Q)
        f       = Q * a / math.cos(alpha)
        k_total = beta_h * h + beta_f * f

        x.append(Q)
        y.append(k_total)

        print "%f %f" % (Q, k_total)

    print 'approximate solution = %s (Q = %s)' % (min(y), x[y.index(min(y))])

def run():
    for i in range(0, 1):
        get_derivative(a = 121, alpha = 5)

# docs: http://docs.python.org/library/profile.html
import cProfile, pstats
profile_file = '../data/profile.txt'
cProfile.run('run()', profile_file)
p = pstats.Stats(profile_file)
p.strip_dirs()
#p.sort_stats('cumulative')
p.sort_stats('time')
p.print_stats(30)