#!/usr/bin/env python
"""Simulation bootstrapper"""

from formation_flight.formation import handlers as formation_handlers
from formation_flight.aircraft import handlers as aircraft_handlers
from formation_flight.aircraft import generators
from formation_flight.hub import builders
from formation_flight.hub import allocators

from lib import sim, debug, sink
from lib.debug import print_line as p

#from formation_flight import visualization
from formation_flight import statistics

import config

#visualization.init()

def run():

    for i in xrange(0, 5):

      sim.init()
      aircraft_handlers.init()
      formation_handlers.init()
      statistics.init()
      sink.init()

      # Construct flight list
      planes = generators.get_via_stdin()
  
      # Find hubs
      hubs = builders.build_hubs(planes, config.count_hubs, config.Z)
  
      # Allocate hubs to flights
      allocators.allocate(planes, hubs)

      for flight in planes:
          sim.events.append(sim.Event('aircraft-init', flight, 0))
  
      sim.run()

# docs: http://docs.python.org/library/profile.html
import cProfile, pstats
profile_file = 'data/profile.txt'
cProfile.run('run()', profile_file)
p = pstats.Stats(profile_file)
p.strip_dirs()
p.sort_stats('cumulative')
p.sort_stats('time')
#p.print_stats(30)
