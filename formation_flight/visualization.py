from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

from lib import sim, debug

flights = []

def handle_depart(event):
    aircraft    = event.sender
    origin      = aircraft.position
    destination = aircraft.route.waypoints[-1]
    flights.append([origin, destination])
    print origin, destination

def init():
    sim.dispatcher.register('aircraft-depart', handle_depart)
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
    
    for flight in flights:
        m.drawgreatcircle(flight[0].lon, flight[0].lat,
                          flight[1].lon, flight[1].lat,
                          linewidth = 1, color='b')
    
    m.drawcoastlines()
    m.fillcontinents()
    m.drawparallels(np.arange(10,90,20), labels = [1,1,0,1])
    m.drawmeridians(np.arange(-180,180,30), labels = [1,1,0,1])
    ax.set_title('Flights')
    plt.show()
    
