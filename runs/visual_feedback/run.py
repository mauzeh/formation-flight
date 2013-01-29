#!/usr/bin/env python
"""Simulation bootstrapper"""

from formation_flight.formation import handlers as formation_handlers
from formation_flight.aircraft import handlers as aircraft_handlers
from formation_flight.aircraft import generators
from formation_flight.hub import builders
from formation_flight.hub import allocators
from formation_flight import visualization

from lib import sim, debug, sink
from lib.debug import print_line as p

from formation_flight import statistics

import config
import os
import numpy as np

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import config

from lib.debug import print_line as p

config.count_hubs = 2
config.min_P = 0
config.dt = 10
config.Z = 0.25
config.phi_max = 10

config.map = {
    'parallels' : np.arange(0, 90, 10),
    'meridians' : np.arange(-180, 180, 20)
}

def single_run():

    sim.init()
    aircraft_handlers.init()
    formation_handlers.init()
    statistics.init()

    # Construct flight list
    planes = generators.get_via_stdin()

    # Find hubs
    config.hubs = builders.build_hubs(planes, config.count_hubs, config.Z)

    # Allocate hubs to flights
    allocators.allocate(planes, config.hubs)
    
    for flight in planes:
        sim.events.append(sim.Event('aircraft-init', flight, 0))
    
    sim.run()
    debug.print_dictionary(statistics.vars)
    
    return planes



def render(segments):
    
    # create new figure, axes instances.
    fig = plt.figure()
    ax  = fig.add_axes([0.1,0.1,0.8,0.8], axisbg = '#a5bfdd')
    
    llcrnrlon = config.map_dimensions['lon'][0]
    urcrnrlon = config.map_dimensions['lon'][1]
    
    llcrnrlat = config.map_dimensions['lat'][0]
    urcrnrlat = config.map_dimensions['lat'][1]

    # setup mercator map projection.
    m = Basemap(
        llcrnrlon = llcrnrlon, llcrnrlat = llcrnrlat,
        urcrnrlon = urcrnrlon, urcrnrlat = urcrnrlat,
        rsphere = (6378137.00,6356752.3142),
        resolution = 'c', projection = 'merc',
        #lat_0 = 40.,lon_0 = -20.,lat_ts = 20.
    )
    
    for segment in segments['benchmark']:
        m.drawgreatcircle(segment.start.lon, segment.start.lat,
                          segment.end.lon, segment.end.lat,
                          linewidth = 1, color='#00458A')
        x, y = m(segment.start.lon, segment.start.lat)
        m.plot(x, y, 'bo', ms = 4)
        x, y = m(segment.end.lon, segment.end.lat)
        m.plot(x, y, 'bo', ms = 4)

    for segment in segments['formation']:
        p('geo-debug', 'Start to plot a formation trajectory')
        p('geo-debug', 'Trajectory: (%s, %s) -> (%s, %s)' % (
            segment.start.lon, segment.start.lat,
            segment.end.lon, segment.end.lat
        ))
        m.drawgreatcircle(segment.start.lon, segment.start.lat,
                          segment.end.lon, segment.end.lat,
                          linewidth = 1, color='g')
        x, y = m(segment.start.lon, segment.start.lat)
        m.plot(x, y, 'go', ms = 4)
        x, y = m(segment.end.lon, segment.end.lat)
        m.plot(x, y, 'go', ms = 4)
        p('geo-debug', 'Done with plotting a formation trajectory')
    
    for segment in segments['solo']:
        m.drawgreatcircle(segment.start.lon, segment.start.lat,
                          segment.end.lon, segment.end.lat,
                          linewidth = 1, color='r')
        x, y = m(segment.start.lon, segment.start.lat)
        m.plot(x, y, 'ro', ms = 4)
        x, y = m(segment.end.lon, segment.end.lat)
        m.plot(x, y, 'ro', ms = 4)

    m.drawcoastlines(color='#8f8457')
    m.fillcontinents(color='#f5f0db')
    m.drawcountries(color='#a9a06d')
    m.drawparallels(config.map['parallels'], labels = [1,1,0,1])
    m.drawmeridians(config.map['meridians'], labels = [1,1,0,1])
    
    return plt, ax