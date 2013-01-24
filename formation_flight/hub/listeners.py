"""Hub listeners capture hub aircraft flow rates"""

import config

from lib import sim
from lib.debug import print_line as p
from lib.debug import print_dictionary
from lib.util import round_float

import numpy as np
import math

vars = {}
interval_length = 30

import matplotlib.pyplot as plt

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

    #plt.rc(('xtick.major', 'ytick.major'), pad = 10)
    
    plt.bar(
        timestamps,
        values,
        width = interval_length - 5,
        linewidth = 0,
        color = '#999999'
    )
    
    plt.title(r'Traffic Density at hub $(P_{min}=%s)$' % config.min_P)
    plt.xlabel(r'Time of day (UTC)')#, labelpad = 20)
    plt.ylabel(r'Number of flights')#, labelpad = 20)
    
    plt.xlim(0, 1440)
    plt.ylim(0, 30)
    
    plt.xticks(
        [0,
         180,
         360,
         540,
         720,
         900,
         1080,
         1260,
         1440],
        ['00:00',
         '03:00',
         '06:00',
         '09:00',
         '12:00',
         '15:00',
         '18:00',
         '21:00',
         '00:00']
    )
    
    plt.show()
