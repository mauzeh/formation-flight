from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt

import math

from lib.geo.util import midpoint, project_segment
from lib.geo.point import Point
from lib.geo.waypoint import Waypoint
from lib.geo.segment import Segment

from lib.debug import print_object

class Viz:
    
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
    
    def plot_point(self, point, formatting = 'go'):
        x, y = self.map(point.lon, point.lat)
        self.map.plot(x, y, formatting, ms = 8)
        
    def plot_great_circle(self, segment, color = 'b'):
        point1 = segment.start
        point2 = segment.end
        self.map.drawgreatcircle(
            point1.lon, point1.lat,
            point2.lon, point2.lat,
            linewidth = 1.5, color=color)

    def render(self):
        self.map.drawcoastlines(color='#8f8457')
        self.map.fillcontinents(color='#f5f0db')
        self.map.drawcountries(color='#a9a06d')
        self.map.drawparallels(np.arange(10,90,20), labels = [1,1,0,1])
        self.map.drawmeridians(np.arange(-180,180,30), labels = [1,1,0,1])
        self.ax.set_title('Flights')
        plt.show()
        
def construct_hub(origins, destinations, Z):

    midpoint_origins = midpoint(origins)
    midpoint_destinations = midpoint(destinations)

    hub_route = Segment(midpoint_origins, midpoint_destinations)
    
    return hub_route.start.get_position(
        hub_route.get_initial_bearing(),
        hub_route.get_length() * Z)

def rank_origins(origins, destinations):

    midpoint_origins = midpoint(origins)
    midpoint_destinations = midpoint(destinations)
    hub_route = Segment(midpoint_origins, midpoint_destinations)
    for origin in origins:
        
        AC = Segment(midpoint_origins, origin)
        orthogonal_heading = hub_route.get_initial_bearing() + 90    
        (a, b) = project_segment(
            abs(orthogonal_heading - AC.get_initial_bearing()),
            AC.get_length()
        )
        projection = midpoint_origins.get_position(
            orthogonal_heading, a
        )
        midpoint_to_projection = Segment(
            midpoint_origins,
            projection
        )
        
        angle = abs(
            hub_route.get_initial_bearing() - 
            midpoint_to_projection.get_initial_bearing()
        )
        if abs(angle - 90) < 0.1:
            distance = -1 * midpoint_to_projection.get_length()
        else:
            distance = midpoint_to_projection.get_length()
        origin.distance_to_midpoint = distance
        
    return sorted(origins, key = lambda point: point.distance_to_midpoint)

def run():
    
    origins = [
        Waypoint('CPH'),
        Waypoint('TXL'),
        Waypoint('OSL'),
        Waypoint('HEL'),
        Waypoint('ARN'),
        Waypoint('MUC'),
        Waypoint('MAD'),
        Waypoint('AMS'),
        Waypoint('DUB'),
        Waypoint('BRU'),
        Waypoint('CDG'),
        Waypoint('DUS'),
        Waypoint('FRA'),
        Waypoint('ATH'),
        Waypoint('MAN'),
        Waypoint('FCO'),
        Waypoint('LHR')
    ]
    
    destinations = [
        Waypoint('JFK'),
        Waypoint('SFO'),
        Waypoint('EWR'),
        Waypoint('BOS'),
        Waypoint('PHL'),
        Waypoint('ATL'),
        Waypoint('MIA'),
        Waypoint('MCO'),
        Waypoint('LAX'),
        Waypoint('SFO'),
        Waypoint('ORD'),
        Waypoint('SEA'),
        Waypoint('YVR'),
        Waypoint('IAD'),
    ]
    
    origins_ranked = rank_origins(origins, destinations)
    
    n = 3
    origin_set_size = len(origins) / n
    origin_chunks = [list(t) for t in zip(*[iter(origins_ranked)]*origin_set_size)]
    
    viz = Viz()
    for point in destinations:
        viz.plot_point(point)

    for Z in [.2]:
        for origins in origin_chunks:
            hub = construct_hub(origins, destinations, Z)
            viz.plot_point(hub, formatting = 'bo')
            for point in origins:
                viz.plot_great_circle(Segment(point, hub))
                viz.plot_point(point)
    
    viz.render()
