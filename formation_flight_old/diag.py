from formation_flight.aircraft import Aircraft
from formation_flight.formation import Formation
from lib import debug

count = 0

# Only respond to these signals
signals = [
    'aircraft-depart',
    'formation-lock',
    'aircraft-arrive',
]

def register():
    print 'still need to hook the events up to diag.py'
    #dispatcher.connect(handle)

def get_debug_info(data):

    lines = []

    if type(data) is Aircraft:

        segment = data.route.get_current_segment(data.get_distance_flown())
        d       = data.route.get_distance_into_current_segment(data.get_distance_flown())

        lines.append(('Aircraft', data.name))
        lines.append(('Departure time', data.departure_time))
        lines.append(('Speed', '%.1f' % data._speed))
        lines.append(('Segment', segment))
        lines.append(('Distance into segment', '%.1f' % d))
        lines.append(('Waypoint ETA', '%.1f' % data.get_waypoint_eta()))

    elif type(data) is Formation:
        lines.append(('Participants', data.aircraft))
        lines.append(('Start ETA', '%.2f' % data.get_start_eta()))
        lines.append(('Status', data.status))
        lines.append(('Hub', data.hub if hasattr(data, 'hub') else None))
        pass

    else:
        lines.append(('Data', data))

    return lines
    
def handle(signal, sender, data = None, time = 0):

    if signal not in signals:
        return 0

    global count
    if signal == "formation-init":
        count = count + 1
        print count
        
    lines = []
    headers = []

    headers.append(('Time', '%d' % time))
    headers.append((sender.__class__.__name__, signal))

    debug.print_table(headers, get_debug_info(data))