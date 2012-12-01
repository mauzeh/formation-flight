"""A discrete event simulation framework."""

import debug, config

class Event(object):
    """An occurrence initiated from within the simulation."""

    def __init__(self, label, sender, bubble_time = 0):

        assert bubble_time >= time

        self.label = label
        self.sender = sender
        self.time = bubble_time

    def __repr__(self):
        return '%s (t = %.5f, s = %s)' % (self.label, self.time, self.sender)
        
class Dispatcher(object):
    """Allows functions to be called when an event occurs."""

    def __init__(self):
        self.listeners = {}

    def register(self, event_label, listener):
        """Register a function to be called when an event occurs."""
        if event_label not in self.listeners:
            self.listeners[event_label] = []
        self.listeners[event_label].append(listener)

    def bubble(self, event):
        """Execute registered listeners. Do not call from outside."""
        log_event(event)
        if event.label not in self.listeners:
            return
        for listener in self.listeners[event.label]:
            listener(event)

def log_event(event):
    """Print a log message to standard output when events occur."""
    if event.label not in config.events_printed:
        return
    headers = [
        ('Time', '%d' % time),
        (event.sender.__class__.__name__, event.label)
    ]
    debug.print_object(event.sender, headers = headers)

time = 0
events = []
dispatcher = Dispatcher()

def init():
    global time, events, dispatcher
    time = 0
    events = []
    dispatcher = Dispatcher()

def run():
    """Enumerate events and bubble each until no more events exist.

    Events live in the events list (sim.events), which can be altered at
    will, including while the simulation is running.
    """
    global time, events, dispatcher

    # First fire a 'start sim' event just before the first actual event
    event = min(events, key = lambda e: e.time)
    dispatcher.bubble(Event('sim-start', None, event.time))
    
    while len(events) > 0:
        event = min(events, key = lambda e: e.time)
        global time
        assert event.time >= time

        time = event.time
        events.remove(event)
        dispatcher.bubble(event)

    # Fire a 'sim-finish' event for any post processors (statistics etc).
    dispatcher.bubble(Event('sim-finish', None, time))