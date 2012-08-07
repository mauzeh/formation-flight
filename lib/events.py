from pydispatch import dispatcher
from formation_flight.aircraft import Aircraft

class EventHandler:
    """
    Keeps track of all events in the system and prints them for debugging
    purposes.
    """

    def __init__(self):

        dispatcher.connect(self.handle)

        # Do not respond to these signals
        self.ignore = []#['waypoint-reached']

    def handle(self, signal, sender, data = None, time = 0):

        if(signal in self.ignore):
            return 0

        debug = []

        print '+-----------------------------------------------------+'
        print '| %s :: %s' % (sender.__class__.__name__, signal)
        print '+-----------------------------------------------------+'
        debug.append(('| % 25s: %s units', ('Time', time)))

        if type(data) == Aircraft:

            segment = data.route.get_current_segment(data.get_distance_flown())
            l       = segment.get_length()
            d       = data.route.get_distance_into_current_segment(data.get_distance_flown())
            eta     = time + (l - d) / data.speed

            debug.append(('| % 25s: %s', ('Aircraft', data.name)))
            debug.append(('| % 25s: %.1f', ('Speed', data.speed)))
            debug.append(('| % 25s: %s (%.1f km)', ('Segment', segment, l)))
            debug.append(('| % 25s: %.1f km', ('Distance into segment', d)))
            debug.append(('| % 25s: %.1f', ('Waypoint ETA', eta)))

        else:
            print '| Data: %s' % data

        for line in debug:
            format, data = line
            print format % data
        print '+-----------------------------------------------------+'