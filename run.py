#!/usr/bin/env python
"""Simulation Bootstrapper"""

from runs.normal import run

# docs: http://docs.python.org/library/profile.html
import cProfile, pstats
profile_file = 'data/profile.txt'
cProfile.run('run.execute()', profile_file)
p = pstats.Stats(profile_file)
p.strip_dirs()
p.sort_stats('cumulative')
p.sort_stats('time')
#p.print_stats(30)