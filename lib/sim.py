import debug
import config

class EventList(list):

    def remove_by_label(self, label):
        # It's tempting to just loop and use self.remove(event), but it has 
        # unexpected results so we use enumerate() and remove by index.
        for i, event in enumerate(self):
            if event.label == label:
                del self[i]

class Event(object):
    
    def __init__(self, label, sender, bubble_time = 0):

        assert bubble_time >= time

        self.label = label
        self.sender = sender
        self.time = bubble_time

    def __repr__(self):
        return self.label
        
    def __cmp__(self, other):
        """Allows for easy retrieval of earliest elements (having min(time))"""
        return cmp(self.time, other.time)

class Dispatcher(object):

    def __init__(self):
        self.listeners = {}

    def register(self, event_label, listener):
        if event_label not in self.listeners:
            self.listeners[event_label] = []
        self.listeners[event_label].append(listener)

    def bubble(self, event):
        log_event(event)
        if event.label not in self.listeners:
            return
        for listener in self.listeners[event.label]:
            listener(event)

def log_event(event):

    if event.label not in config.events_printed:
        return

    headers = []
    lines = []

    headers.append(('Time', '%d' % time))
    headers.append((event.sender.__class__.__name__, event.label))

    for key in event.sender.__dict__:
        lines.append((key, event.sender.__dict__[key]))

    debug.print_table(headers, lines)

time = 0
events = EventList()
dispatcher = Dispatcher()
    
def run():
    while len(events) > 0:
        event = min(events)
        global time
        assert event.time >= time

        time = event.time
        events.remove(event)
        dispatcher.bubble(event)