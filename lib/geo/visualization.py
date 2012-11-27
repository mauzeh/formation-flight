from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

from lib.geo.point import Point
from lib.geo.segment import Segment
from lib.geo.route import Route

class GCMapper:
    def __init__(self):
        # create new figure, axes instances.
        self.fig = plt.figure()
        self.ax  = self.fig.add_axes([0.1,0.1,0.8,0.8], axisbg = '#a5bfdd')
        
        # setup mercator map projection.
        self.map = Basemap(llcrnrlon = -130., llcrnrlat = 1.,
                    urcrnrlon = 40.,   urcrnrlat = 70.,
                    rsphere = (6378137.00,6356752.3142),
                    resolution = 'c',
                    projection = 'merc',
                    lat_0 = 40.,lon_0 = -20.,lat_ts = 20.)
        
    def plot(self, element):
        if isinstance(element, Segment):
            self.plot_segment(element)
        if isinstance(element, Route):
            self.plot_route(element)
        if isinstance(element, Point):
            self.plot_point(element)
        raise Exception('Incompatible type %s of element to plot' % type(element))
        
    def plot_route(self, route, color = 'b', linestyle = '-'):
        #just to be suer
        route.init_segments()
        for segment in route.segments:
            self.plot_segment(segment, color = color, linestyle = linestyle)
    
    def plot_point(self, point, formatting = 'go'):
        x, y = self.map(point.lon, point.lat)
        self.map.plot(x, y, formatting, ms = 8)
        
    def plot_segment(self, segment, color = 'b', linestyle = '-'):
        point1 = segment.start
        point2 = segment.end
        self.map.drawgreatcircle(
            point1.lon, point1.lat,
            point2.lon, point2.lat,
            linestyle = linestyle,
            linewidth = 1.5,
            color = color)

    def render(self):
        self.map.drawcoastlines(color='#8f8457')
        self.map.fillcontinents(color='#f5f0db')
        self.map.drawcountries(color='#a9a06d')
        self.map.drawparallels(np.arange(10,90,20), labels = [1,1,0,1])
        self.map.drawmeridians(np.arange(-180,180,30), labels = [1,1,0,1])
        self.ax.set_title('Flights')
        plt.show()