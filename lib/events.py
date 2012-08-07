from pydispatch import dispatcher
from formation_flight.aircraft import Aircraft
from formation_flight.formation import Formation

class EventHandler:
    """
    Keeps track of all events in the system and prints them for debugging
    purposes.
    """

    def __init__(self):

        dispatcher.connect(self.handle)

        # Do not respond to these signals
        self.ignore = ['fly', 'sim-init']

    def handle(self, signal, sender, data = None, time = 0):

        if(signal in self.ignore):
            return 0

        debug = []

        print '+-----------------------------------------------------+'
        print '| Time: %d units' % time
        print '| %s: %s' % (sender.__class__.__name__, signal)
        print '+-----------------------------------------------------+'

        if type(data) == Aircraft:

            segment = data.route.get_current_segment(data.get_distance_flown())
            l       = segment.get_length()
            d       = data.route.get_distance_into_current_segment(data.get_distance_flown())
            eta     = time + (l - d) / data.speed

            debug.append(('| % 25s: %s', ('Aircraft', data.name)))
            debug.append(('| % 25s: %s', ('Departure time', data.departure_time)))
            debug.append(('| % 25s: %.1f', ('Speed', data.speed)))
            debug.append(('| % 25s: %s (%.1f km)', ('Segment', segment, l)))
            debug.append(('| % 25s: %.1f km', ('Distance into segment', d)))
            debug.append(('| % 25s: %.1f', ('Waypoint ETA', data.get_waypoint_eta())))

        elif type(data) == Formation:
            debug.append(('| %25s: %s', ('Participants', data.aircraft)))
            debug.append(('| %25s: %.2f', ('Start ETA', data.get_start_eta())))
            debug.append(('| %25s: %s', ('Status', data.status)))
            pass

        else:
            print '| Data: %s' % data

        for line in debug:
            format, data = line
            print format % data
        print '+-----------------------------------------------------+'