import debug
from operator import attrgetter
import config

class Event(object):
    
    def __init__(self, label, sender, bubble_time = 0):

        assert bubble_time >= time

        self.label = label
        self.sender = sender
        self.time = bubble_time

    def __repr__(self):
        return '%s (t = %d, s = %s)' % (self.label, self.time, self.sender)
        
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
    headers.append(('Time', '%d' % time))
    headers.append((event.sender.__class__.__name__, event.label))

    debug.print_object(event.sender, headers = headers)

time = 0
events = []
dispatcher = Dispatcher()
    
def run():
    while len(events) > 0:
        event = min(events, key = attrgetter('time'))
        global time
        assert event.time >= time

        time = event.time
        events.remove(event)
        dispatcher.bubble(event)
