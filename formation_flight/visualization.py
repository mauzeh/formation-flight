from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

from lib.geo.segment import Segment

from lib import sim, debug

segments = []
waypoints = []

def handle_init(event):
    aircraft = event.sender
    segments.append(aircraft.route.segments[0])
    waypoints.append(aircraft.route.waypoints[0])
    waypoints.append(aircraft.route.waypoints[1])

def handle_at_waypoint(event):
    aircraft = event.sender
    if aircraft.position not in waypoints:
        waypoints.append(aircraft.position)
        
def handle_alive(event):
    formation = event.sender
    for aircraft in formation:
        segments.append(Segment(formation.hub, aircraft.route.waypoints[0]))
        segments.append(aircraft.route.segments[0])
        waypoints.append(aircraft.route.waypoints[1])

def init():
    sim.dispatcher.register('aircraft-init', handle_init)
    sim.dispatcher.register('aircraft-at-waypoint', handle_at_waypoint)
    sim.dispatcher.register('formation-alive', handle_alive)
    sim.dispatcher.register('sim-finish', render)

def render(event):
    # create new figure, axes instances.
    fig = plt.figure()
    ax  = fig.add_axes([0.1,0.1,0.8,0.8])
    
    # setup mercator map projection.
    m = Basemap(llcrnrlon = -130., llcrnrlat = 1.,
                urcrnrlon = 40.,   urcrnrlat = 70.,
                rsphere = (6378137.00,6356752.3142),
                resolution = 'l',
                projection = 'merc',
                lat_0 = 40.,lon_0 = -20.,lat_ts = 20.)
    
    for segment in segments:
        m.drawgreatcircle(segment.start.lon, segment.start.lat,
                          segment.end.lon, segment.end.lat,
                          linewidth = 1, color='b')
        
    for waypoint in waypoints:
        x, y = m(waypoint.lon, waypoint.lat)
        m.plot(x, y, 'bo', ms = 8)
    
    m.drawcoastlines()
    m.fillcontinents()
    m.drawparallels(np.arange(10,90,20), labels = [1,1,0,1])
    m.drawmeridians(np.arange(-180,180,30), labels = [1,1,0,1])
    ax.set_title('Flights')
    plt.show()