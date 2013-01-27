"""Hub listeners capture hub aircraft flow rates"""

import os
import config

from lib import sim
from lib.debug import print_line as p
from lib.debug import print_dictionary
from lib.util import round_float
from lib.util import make_sure_path_exists

import matplotlib.pyplot as plt
import matplotlib

import numpy as np
import math

vars = {}
interval_length = 30

font = {'size' : 20}
matplotlib.rc('font', **font)

def init(hubs):

    assert len(hubs) > 0

    sim.dispatcher.register('aircraft-at-waypoint', handle_at_waypoint)
    sim.dispatcher.register('sim-finish', handle_finish)

    # Also set an event that clears the aircraft each $interval mins
    for i in np.arange(0, 24*60 + interval_length, interval_length):
        sim.events.append(sim.Event(
            'clear-hub-queue',
            'hub',
            float(i)
        ))
        vars[i] = 0

def handle_at_waypoint(event):

    aircraft = event.sender
    
    # Discard flight times above end of day (midnight)
    if event.time > 1440:
        return

    # Round the time so we can group the flights into time buckets
    index = round_float(event.time - float(interval_length)/2, interval_length)

    if aircraft.position == aircraft.hub:
        vars[index] += 1

def handle_finish(event):
    plot_flow_rate(vars)

def plot_flow_rate(data):

    timestamps = []
    values     = []
    
    for key in sorted(data.iterkeys()):
        timestamps.append(key)
        values.append(data[key])
    
    # For testing/debugging
    #timestamps = np.arange(0, 1440, 60)
    #values = np.linspace(0, 35, len(timestamps))

    time_labels = []

    for timestamp in timestamps:
    
        # Normalize time to be reset after midnight (if > 1440, then subtract 1440)
        timestamp = timestamp % 1440
        hours     = math.floor(timestamp / 60)
        minutes   = math.floor(timestamp - hours * 60)
        
        time_labels.append('%02d:%02d' % (hours, minutes))

    plt.rc(('xtick.major', 'ytick.major'), pad = 10)
    
    plt.bar(
        timestamps,
        values,
        width = interval_length - 5,
        linewidth = 0,
        color = '#999999'
    )
    
    t = plt.title(r'Traffic Density at hub ($C_{min}=%s$)' % config.min_P)
    t.set_y(1.03) 
    plt.subplots_adjust(top = 0.85, bottom = 0.2) 
    
    plt.xlabel(r'Time of day (UTC)', labelpad = 10)
    plt.ylabel(r'Number of flights', labelpad = 5)
    
    plt.xlim(0, 1440)
    plt.ylim(0, 40)
    
    xt = plt.xticks(
        [0,
         240,
         480,
         720,
         960,
         1200,
         1440],
        ['00:00',
         '04:00',
         '08:00',
         '12:00',
         '16:00',
         '18:00',
         '22:00',
         '00:00']
    )
    
    fig_path = '%s/plot_%s.pdf' % (
        config.sink_dir,
        str(config.min_P).replace('.','_')
    )
    fig_path = fig_path.replace('/runs/', '/plots/')
    fig_path = fig_path.replace('/sink/', '/')
    
    make_sure_path_exists(os.path.dirname(fig_path))
    
    #plt.show()
    plt.savefig(
        fig_path,
        bbox_inches='tight'
    )
