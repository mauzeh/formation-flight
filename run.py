#!/usr/bin/env python
"""Simulation Bootstrapper"""

from runs.singlehub.validation import run
run.execute()

#from runs.multihub.L_s_2hubs  import run
#run.execute()
#
#from runs.multihub.L_s_5hubs  import run
#run.execute()
#
#from runs.multihub.L_s_10hubs  import run
#run.execute()
#
#from runs.multihub.L_Z_2hubs  import run
#run.execute()
#
#from runs.multihub.L_Z_5hubs  import run
#run.execute()
#
#from runs.multihub.L_Z_10hubs  import run
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