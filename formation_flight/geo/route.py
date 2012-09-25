from formation_flight.geo.point import Position
from formation_flight.geo.segment import Segment

class Route(object):
    """A collection of segments"""
    def __init__(self, waypoints = []):
        self.segments = []
        previous_waypoint = None
        for waypoint in waypoints:
            if previous_waypoint is not None:
                self.segments.append(Segment(previous_waypoint, waypoint))
            previous_waypoint = waypoint

    def get_segments_flown(self, distance_flown):
        segments_flown = []
        cumulative_distance = 0
        for segment in self.segments:
            cumulative_distance = cumulative_distance + segment.get_length()
            if cumulative_distance > distance_flown:
                break
            segments_flown.append(segment)
        return segments_flown

    def get_current_segment(self, distance_flown):
        segments_flown = self.get_segments_flown(distance_flown)
        assert isinstance(segments_flown, list)
        return self.segments[len(segments_flown)]

    def get_distance_into_current_segment(self, distance_flown):

        segments_flown = self.get_segments_flown(distance_flown);
        distance_into_segment = distance_flown

        assert isinstance(segments_flown, list)

        for segment in segments_flown:
            distance_into_segment = distance_into_segment - segment.get_length()

        return distance_into_segment

    def get_segments(self):
        return self.segments

    def get_length(self):
        length = 0
        for segment in self.segments:
            length = length + segment.get_length()
        return length

    def get_current_position(self, distance_flown):

        distance_flown_in_cur = self.get_distance_into_current_segment(distance_flown)
        current_segment = self.get_current_segment(distance_flown)
        bearing = current_segment.initial_bearing

        if(distance_flown_in_cur == 0):
            return Position(current_segment.start.lat, current_segment.start.lon, bearing)

        return current_segment.start.get_position(bearing, distance_flown_in_cur)

    def get_destination(self):
        return self.segments[len(self.segments)-1].end

    def __repr__(self):
        return '%s' % self.segments