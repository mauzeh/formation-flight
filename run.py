#!/usr/bin/env python
"""Simulation Bootstrapper"""

from runs.singlehub.z import run
run.execute()

#from runs.multihub.n_phi import run
#run.execute()
#from runs.multihub.n_s import run
#run.execute()
#from runs.multihub.n_pmin import run
#run.execute()
#from runs.multihub.n_z import run
#run.execute()
#from runs.multihub.n_dt import run
#run.execute()
#from runs.multihub.pmin_phi import run
#run.execute()
#from runs.multihub.L_Z_3hubs import run
#run.execute()
#from runs.multihub.n_alpha import run
#run.execute()

## docs: http://docs.python.org/library/profile.html
#import cProfile, pstats
#profile_file = 'data/profile.txt'
#cProfile.run('run.execute()', profile_file)
#p = pstats.Stats(profile_file)
#p.strip_dirs()
#p.sort_stats('cumulative')
#p.sort_stats('time')
##p.print_stats(30)