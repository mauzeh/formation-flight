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

        lines = []

        lines.append('+-----------------------------------------------------+')
        lines.append('| Time: %d units' % time)
        lines.append('| %s: %s' % (sender.__class__.__name__, signal))
        lines.append('+-----------------------------------------------------+')

        if type(data) == Aircraft:

            segment = data.route.get_current_segment(data.get_distance_flown())
            d       = data.route.get_distance_into_current_segment(data.get_distance_flown())

            lines.append('| % 25s: %s' % ('Aircraft', data.name))
            lines.append('| % 25s: %s' % ('Departure time', data.departure_time))
            lines.append('| % 25s: %.1f' % ('Speed', data.speed))
            lines.append('| % 25s: %s' % ('Segment', segment))
            lines.append('| % 25s: %.1f km' % ('Distance into segment', d))
            lines.append('| % 25s: %.1f' % ('Waypoint ETA', data.get_waypoint_eta()))

        elif type(data) == Formation:
            lines.append('| %25s: %s' % ('Participants', data.aircraft))
            lines.append('| %25s: %.2f' % ('Start ETA', data.get_start_eta()))
            lines.append('| %25s: %s' % ('Status', data.status))
            pass

        else:
            print '| Data: %s' % data

        # output table width (in chars)
        width = 55
        for line in lines:
            line_len = len(line)
            end_line = '' if line_len >= width else "|"
            print line + ' ' * (width - line_len - 1) + end_line
        print '+-----------------------------------------------------+'