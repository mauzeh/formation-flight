from .point import *
import csv

class Waypoint(Point):

    def __init__(self, code):

        reader = csv.reader(open('data/waypoints.csv'))
        for row in reader:
            if(code == row[0]):
                super(Waypoint, self).__init__(float(row[1]), float(row[2]), row[0])

    def __repr__(self):
        return '%s' % self.name