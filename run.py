#!/usr/bin/env python
"""Simulation Bootstrapper"""

from runs._base_single_hub.small_lock import run
    
if __name__ == '__main__':
    run.execute()
    
    ## docs: http://docs.python.org/library/profile.html
    #import cProfile, pstats
    #profile_file = 'data/profile.txt'
    #cProfile.run('run.execute()', profile_file)
    #p = pstats.Stats(profile_file)
    #p.strip_dirs()
    #p.sort_stats('cumulative')
    #p.sort_stats('time')
    ##p.print_stats(30)