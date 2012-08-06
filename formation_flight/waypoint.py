from .point import *
import csv
import os

class Waypoint(Point):

    def __init__(self, code):

        fn = os.path.join(os.path.dirname(__file__), '..', 'data/waypoints.csv')
        reader = csv.reader(open(fn))
        for row in reader:
            if(code == row[0]):
                super(Waypoint, self).__init__(float(row[1]), float(row[2]), row[0])

    def __repr__(self):
        #return '%s' % self.name
        return '%s (%s, %s)' % (self.name, self.lat, self.lon)
