import math

__author__ = 'maurits_dekkers'

class Earth(object):

    # 6371.00 in km, 3440.07 in NM
    # always make sure this is a float!!!
    R = 3440.07

class Point(object):

    """Represents a point on earth. Lat/lon in decimal degrees."""

    lat = 0
    lon = 0
    name = ''

    def __init__(self, lat, lon, name = 'Point'):
        self.lat = lat
        self.lon = lon
        self.name = name

    def distance_to(self, point):
        R = Earth.R
        lat1 = math.radians(self.lat)
        lat2 = math.radians(point.lat)
        lon1 = math.radians(self.lon)
        lon2 = math.radians(point.lon)
        return math.acos(math.sin(lat1)*math.sin(lat2)+
                         math.cos(lat1)*math.cos(lat2)*
                         math.cos(lon2-lon1))*R

    def bearing_to(self, point):
        lat1 = math.radians(self.lat)
        lat2 = math.radians(point.lat)
        lon1 = math.radians(self.lon)
        lon2 = math.radians(point.lon)
        dLon = lon2 - lon1
        y = math.sin(dLon) * math.cos(lat2)
        x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*\
                                            math.cos(lat2)*\
                                            math.cos(dLon)
        return math.degrees(math.atan2(y, x)) % 360

    def __repr__(self):
        #return "%s(%r)" % (self.__class__, self.__dict__)
        return '%s (%s, %s)' % (self.name, self.lat, self.lon)
        #return '%s' % self.name