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

