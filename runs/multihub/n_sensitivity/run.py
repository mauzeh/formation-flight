#!/usr/bin/env python
"""Simulation bootstrapper"""

from formation_flight.formation import handlers as formation_handlers
from formation_flight.aircraft import handlers as aircraft_handlers
from formation_flight.aircraft import generators
from formation_flight.hub import builders
from formation_flight.hub import allocators

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math

from lib import sim, debug, sink
from lib.debug import print_line as p
from lib.util import make_sure_path_exists

from formation_flight import statistics

import config
import os

import numpy as np

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

font = {'size' : 20}
matplotlib.rc('font', **font)

def execute():
    
    sink.init(config.sink_dir)
    
    sinkdata = []
    
    runs = range(0, 10)
    hubs = np.arange(1, 11)
    
    for n in hubs:

        fuelsavings_list = []
        
        for run in runs:

            config.count_hubs = n
            fuel_savings = single_run()
            
            fuelsavings_list.append(fuel_savings)

        sinkdata.append(np.array(fuelsavings_list))

    print '#################################'
    print '############ NOTICE #############'
    print 'This run has a built-in plotter.'
    print '#################################'
    
    means = []
    errors = []
    for hub_savings_list in sinkdata:
        means.append(np.mean(hub_savings_list))
        errors.append(np.std(hub_savings_list))
        
    for i in range(0, len(means)):
        print r'%d & %.4f & %.4f \\' % (
            i+1, means[i], errors[i]
        )
    
    means = np.array(means)
    errors = np.array(errors)
    
    plt.grid(True)
    
    (mean_line, caps, _) = plt.errorbar(
        np.arange(1, len(means)+1),
        means, yerr = errors, elinewidth = 2
    )
    
    mean_line.set_color('#000000')
    
    for cap in caps:
        cap.set_markeredgewidth(2)
    
    plt.xlim(0.5, len(means)+.5)
    plt.xticks(hubs)
    plt.ylim(0, max(means)*1.1)
    plt.title(r'Fuel Saved')
    plt.xlabel(r'Amount of hubs $H$')
    plt.ylabel(r'Fuel Saved $F_s$ [%]')
    
    fig_path = '%s/plot_%s.pdf' % (config.sink_dir, 'fuel_saved')
    fig_path = fig_path.replace('/runs/', '/plots/')
    fig_path = fig_path.replace('/sink/', '/')
    make_sure_path_exists(os.path.dirname(fig_path))
    plt.savefig(
        fig_path,
        bbox_inches='tight'
    )
    
def single_run():

    sim.init()
    aircraft_handlers.init()
    formation_handlers.init()
    statistics.init()
    
    # Construct flight list
    config.planes = generators.get_via_stdin()
    
    # Find hubs
    config.hubs = builders.build_hubs(config.planes, config.count_hubs, config.Z)

    # Allocate hubs to flights
    allocators.allocate(config.planes, config.hubs)
    
    for flight in config.planes:
        sim.events.append(sim.Event('aircraft-init', flight, 0))
    
    sim.run()

    debug.print_dictionary(statistics.vars)
    
    return statistics.vars['fuel_saved']