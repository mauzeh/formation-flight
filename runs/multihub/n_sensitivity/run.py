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

def fuel_saved_abs_formatter(locs, labels):
    return map(lambda x: "%.1f" % x, locs*1e-6)

def execute():
    
    sink.init(config.sink_dir)
    
    reldata = []
    absdata = []
    
    runs = range(0, 25)
    config.simhubs = np.arange(1, 11)
    
    for n in config.simhubs:

        fuelsavings_list = []
        fuelsavings_abs_list = []
        
        for run in runs:

            config.count_hubs = n
            fuel_savings, fuel_savings_abs = single_run()
            
            fuelsavings_list.append(fuel_savings)
            fuelsavings_abs_list.append(fuel_savings_abs)

        reldata.append(np.array(fuelsavings_list))
        absdata.append(np.array(fuelsavings_abs_list))

    print '#################################'
    print '############ NOTICE #############'
    print 'This run has a built-in plotter.'
    print '#################################'
    
    for i in range(0, len(reldata)):
        
        abs_mean = np.mean(absdata[i])
        abs_std  = np.std(absdata[i])

        rel_mean = np.mean(reldata[i])
        rel_std  = np.std(reldata[i])
        
        print r'%d & %.4f & %.4f & %d & %d \\' % (
            i+1,
            rel_mean, rel_std,
            abs_mean, abs_std
        )
    
    do_plot(
        absdata,
        filename = 'fuel_saved_abs',
        title = r'Fuel Saved [$10^6$ kg]',
        ylabel = r'Fuel Saved [$10^6$ kg]',
        formatter = fuel_saved_abs_formatter
    )

    do_plot(
        reldata,
        filename = 'fuel_saved_rel',
        title = r'Fuel Saved [%]',
        ylabel = r'Fuel Saved [%]'
    )
    
def do_plot(data, title, ylabel, filename, formatter = None):
    
    means = []
    errors = []
    for hub_savings_list in data:
        means.append(np.mean(hub_savings_list))
        errors.append(np.std(hub_savings_list))

    means = np.array(means)
    errors = np.array(errors)
    
    plt.figure()
    plt.grid(True)
    
    (mean_line, caps, _) = plt.errorbar(
        np.arange(1, len(means)+1),
        means, yerr = errors, elinewidth = 2
    )

    mean_line.set_color('#000000')
    
    for cap in caps:
        cap.set_markeredgewidth(2)
    
    plt.xlim(0.5, len(means)+.5)
    plt.xticks(config.simhubs)
    plt.ylim(0, max(means)*1.1)
    plt.title(title)
    plt.xlabel(r'Number of hubs $H$')
    plt.ylabel(ylabel)
    
    if formatter is not None:
        locs, labels = plt.yticks()
        plt.yticks(locs, formatter(locs, labels))
    
    fig_path = '%s/%s.pdf' % (config.sink_dir, filename)
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
    
    return statistics.vars['fuel_saved'], statistics.vars['fuel_saved_abs']