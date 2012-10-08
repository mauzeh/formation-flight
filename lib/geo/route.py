from lib.geo.point import Position
from lib.geo.segment import Segment

class Route(object):
    """A collection of segments"""
    def __init__(self, waypoints = []):
        self.waypoints = waypoints
        self.init_segments()
            
    def init_segments(self):
        """Uses the waypoint list to generate the segments in this route"""
        self.segments = []
        previous_waypoint = None
        for waypoint in self.waypoints:
            if previous_waypoint is not None:
                self.segments.append(Segment(previous_waypoint, waypoint))
            previous_waypoint = waypoint

    def get_segments(self):
        #self.init_segments()
        return self.segments

    def get_length(self):
        #self.init_segments()
        length = 0
        for segment in self.segments:
            length = length + segment.get_length()
        return length

    def get_destination(self):
        #self.init_segments()
        return self.segments[len(self.segments)-1].end

    def __repr__(self):
        #self.init_segments()
        return '%s' % self.segments