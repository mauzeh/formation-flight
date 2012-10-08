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

    def get_segments_flown(self, distance_flown):

        if distance_flown == 0:
            return []

        #self.init_segments()
        segments_flown = []
        cumulative_distance = 0
        for segment in self.segments:
            cumulative_distance = cumulative_distance + segment.get_length()
            if cumulative_distance > distance_flown:
                break
            segments_flown.append(segment)
        return segments_flown

    def get_current_segment(self, distance_flown):
        """Returns the current segment given a certain total distance flown.

        If not flying yet (distance_flown = 0), return first segment.
        If landed (distance_flown > length), return last segment.
        Anything else: return current segment.
        """
        #self.init_segments()

        if distance_flown <= 0:
            return self.segments[0]

        segments_flown = self.get_segments_flown(distance_flown)
        assert isinstance(segments_flown, list)

        # Either return the last of the flown segments. If landed,
        if len(segments_flown) > 0:
            return segments_flown[-1]

        # If we are flying but haven't completed any segments:
        else:
            return self.segments[0]


    def get_distance_into_current_segment(self, distance_flown):
        #self.init_segments()

        segments_flown = self.get_segments_flown(distance_flown);
        distance_into_segment = distance_flown

        assert isinstance(segments_flown, list)

        for segment in segments_flown:
            distance_into_segment = distance_into_segment - segment.get_length()

        return distance_into_segment

    def get_segments(self):
        #self.init_segments()
        return self.segments

    def get_length(self):
        #self.init_segments()
        length = 0
        for segment in self.segments:
            length = length + segment.get_length()
        return length

    def get_current_position(self, distance_flown):
        #self.init_segments()

        distance_flown_in_cur = self.get_distance_into_current_segment(distance_flown)
        current_segment = self.get_current_segment(distance_flown)
        bearing = current_segment.initial_bearing

        if(distance_flown_in_cur == 0):
            return Position(current_segment.start.lat, current_segment.start.lon, bearing)

        return current_segment.start.get_position(bearing, distance_flown_in_cur)

    def get_destination(self):
        #self.init_segments()
        return self.segments[len(self.segments)-1].end

    def __repr__(self):
        #self.init_segments()
        return '%s' % self.segments