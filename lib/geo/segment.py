class Segment(object):
    """
    Represents a line between a start and end point
    """

    def __init__(self, start, end):
        
        # Points that are really close may cause plotting errors, so we
        # let them coincide instead
        if abs(start.lat - end.lat) < .01 and abs(start.lon - end.lon) < .01:
            start.lat = end.lat
            start.lon = end.lon
            #raise Exception('Segment too short: (%s, %s) -> (%s, %s)' % (
            #    start.lat, start.lon,
            #    end.lat, end.lon
            #))
        
        self.start = start
        self.end   = end
        self.initial_bearing = self.start.bearing_to(self.end)
        self.length = self.start.distance_to(self.end)
        self.midpoint = self.start.get_position(self.initial_bearing,
                                                self.length/2)

    def get_length(self):
        return self.length
        
    def get_initial_bearing(self):
        return self.initial_bearing

    def __repr__(self):
        #return "%s -> %s (%s deg)" % (self.start, self.end, self.initial_bearing)
        #return "%s-%s (%.1f)" % (self.start, self.end, self.get_length())
        return '%s-%s' % (self.start, self.end)