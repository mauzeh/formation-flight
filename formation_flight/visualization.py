from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

from lib.geo.segment import Segment
from lib.geo.route import Route
from lib import sim, debug
from lib.debug import print_line as p

segments = {
    'formation' : [],
    'solo'      : []
}

def init():
    sim.dispatcher.register('aircraft-init', handle_init)
    sim.dispatcher.register('aircraft-at-waypoint', handle_at_waypoint)
    sim.dispatcher.register('formation-alive', handle_alive)
    sim.dispatcher.register('aircraft-arrive', handle_arrive)
    sim.dispatcher.register('sim-finish', render)

def handle_init(event):
    pass
    
def handle_at_waypoint(event):
    pass

def handle_alive(event):
    pass

def handle_arrive(event):
    aircraft = event.sender
    route = Route(aircraft.waypoints_passed)
    p('After arrival, the aircraft has passed the following waypoints: %s' % (
        aircraft.waypoints_passed
    ))
    if hasattr(aircraft, 'formation'):
        for segment in route.segments:
            segments['formation'].append(segment)
    else:
        for segment in route.segments:
            segments['solo'].append(segment)

def render(event):
    # create new figure, axes instances.
    fig = plt.figure()
    ax  = fig.add_axes([0.1,0.1,0.8,0.8], axisbg = '#a5bfdd')
    
    # setup mercator map projection.
    m = Basemap(llcrnrlon = -130., llcrnrlat = 1.,
                urcrnrlon = 40.,   urcrnrlat = 70.,
                rsphere = (6378137.00,6356752.3142),
                resolution = 'c',
                projection = 'merc',
                lat_0 = 40.,lon_0 = -20.,lat_ts = 20.)
    
    for segment in segments['solo']:
        m.drawgreatcircle(segment.start.lon, segment.start.lat,
                          segment.end.lon, segment.end.lat,
                          linewidth = 1.5, color='r')
        x, y = m(segment.start.lon, segment.start.lat)
        m.plot(x, y, 'ro', ms = 8)
        x, y = m(segment.end.lon, segment.end.lat)
        m.plot(x, y, 'ro', ms = 8)

    for segment in segments['formation']:
        m.drawgreatcircle(segment.start.lon, segment.start.lat,
                          segment.end.lon, segment.end.lat,
                          linewidth = 1.5, color='g')
        x, y = m(segment.start.lon, segment.start.lat)
        m.plot(x, y, 'go', ms = 8)
        x, y = m(segment.end.lon, segment.end.lat)
        m.plot(x, y, 'go', ms = 8)
    
    m.drawcoastlines(color='#8f8457')
    m.fillcontinents(color='#f5f0db')
    m.drawcountries(color='#a9a06d')
    m.drawparallels(np.arange(10,90,20), labels = [1,1,0,1])
    m.drawmeridians(np.arange(-180,180,30), labels = [1,1,0,1])
    ax.set_title('Flights')
    plt.show()