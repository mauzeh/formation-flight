"""Hub listeners capture hub aircraft flow rates"""

from lib import sim
from lib.debug import print_line as p
from lib.debug import print_dictionary
from lib.util import round_float

import numpy as np

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

#    print_dictionary(vars)

    x = []
    y = []

    for key in sorted(vars.iterkeys()):
        x.append(key)
        y.append(vars[key])

    plt.plot(x, y)
    plt.show()