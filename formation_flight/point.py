import math

__author__ = 'maurits_dekkers'

class Earth(object):

    # 6371.00 in km, 3440.07 in NM
    # always make sure this is a float!!!
    R = 6371.00

class Point(object):

    """Represents a point on earth. Lat/lon in decimal degrees."""

    def __init__(self, lat, lon, name = 'Point', is_virtual_hub = False):
        self.lat = lat
        self.lon = lon
        self.name = name
        self.is_virtual_hub = is_virtual_hub

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

    def get_destination(self, bearing, distance):

        R = Earth.R
        d = distance/R

        theta = math.radians(bearing)

        lat1 = math.radians(self.lat)
        lon1 = math.radians(self.lon)

        part1 = math.cos(d) * math.sin(lat1)
        part2 = math.cos(theta) * math.cos(lat1) * math.sin(d)
        lat2  = math.asin(part1 + part2)

        part3 = math.sin(theta) * math.sin(d) * math.cos(lat1)
        part4 = math.cos(d) - math.sin(lat1) * math.sin(lat2)
        lon2  = lon1 + math.atan2(part3, part4)

        # Normalize between -pi and pi
        lon2  = lon2 - 2 * math.pi * math.floor((lon2 + math.pi) / (2 * math.pi))

        # Calculate the end bearing of the aircraft...
        y = math.sin(lon1 - lon2) * math.cos(lat1)
        x = math.cos(lat2) * math.sin(lat1) - math.sin(lat2) *\
                                              math.cos(lat1) *\
                                              math.cos(lon1 - lon2)
        new_bearing = (math.degrees(math.atan2(y, x)) + 180) % 360
        new_position = Point(math.degrees(lat2), math.degrees(lon2))

        return Position(new_position.lat, new_position.lon, new_bearing)

    def __repr__(self):
        #return "%s(%r)" % (self.__class__, self.__dict__)
        #return '%s (%s, %s)' % (self.name, self.lat, self.lon)
        return '%s' % self.name

class Segment(object):

    def __init__(self, start, end):
        self.start = start
        self.end   = end
        self.initial_bearing = self.start.bearing_to(self.end)
        self.length = self.start.distance_to(self.end)

    def get_length(self):
        return self.length

    def __repr__(self):
        return "%s -> %s (%s deg)" % (self.start, self.end, self.initial_bearing)

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

        return current_segment.start.get_destination(bearing, distance_flown_in_cur)

    def get_destination(self):
        return self.segments[len(self.segments)-1].end

    def __repr__(self):
        return '%s' % self.segments


class Position(Point):

    def __init__(self, lat, lon, bearing):
        super(Position, self).__init__(lat, lon, 'Position')
        self.bearing = bearing

    def __repr__(self):
        return "%r" % (self.__dict__)
