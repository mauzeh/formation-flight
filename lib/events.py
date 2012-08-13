from pydispatch import dispatcher
from formation_flight.aircraft import Aircraft
from formation_flight.formation import Formation, Assigner

class EventHandler:
    """
    Keeps track of all events in the system and prints them for debugging
    purposes.
    """

    def __init__(self):

        dispatcher.connect(self.handle)

        # Do not respond to these signals
        self.ignore = [
            'fly',
            'sim-init',
            'assigner-lock-formations',
            'aircraft-synchronize',
            'formation-init',
            'formation-locked'
        ]

    def handle(self, signal, sender, data = None, time = 0):

        if(signal in self.ignore):
            return 0

        lines = []

        lines.append('+-----------------------------------------------------+')
        lines.append('Time: %d units' % time)
        lines.append('%s: %s' % (sender.__class__.__name__, signal))
        lines.append('+-----------------------------------------------------+')

        if type(data) == Aircraft:
            d = data.route.get_distance_into_current_segment(data.get_distance_flown())
            lines.append('% 25s: %s' % ('Aircraft', data.name))
            lines.append('% 25s: %s' % ('Departure time', data.departure_time))
            lines.append('% 25s: %.1f' % ('Speed', data.speed))
            lines.append('% 25s: %s' % ('Segment', data.get_current_segment()))
            lines.append('% 25s: %.1f km' % ('Distance into segment', d))
            lines.append('% 25s: %.10f' % ('Waypoint ETA', data.get_waypoint_eta()))

        elif type(data) == Formation:
            lines.append('%25s: %s' % ('Participants', data.aircraft))
            lines.append('%25s: %.2f' % ('Start ETA', data.get_start_time()))
            lines.append('%25s: %s' % ('Status', data.status))

        elif type(data) == Assigner:
            lines.append('% 25s: %s' % ('Locked formations', len(data.locked_formations)))
            lines.append('% 25s: %s' % ('Pending formations', len(data.pending_formations)))

        else:
            lines.append('Data: % 10s' % data)

        # output table width (in chars)
        width = 55
        for line in lines:
            line_len = len(line)
            start_line = '' if line_len >= width else "| "
            end_line = '' if line_len >= width else "|"
            repeat = (width - line_len - len(start_line) - len(end_line))
            padding_right = ' ' * repeat
            print start_line + line + padding_right + end_line
        print '+-----------------------------------------------------+'