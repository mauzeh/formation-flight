from pydispatch import dispatcher

class EventHandler:

    def __init__(self):

        dispatcher.connect(self.handle)

        # Do not respond to these signals
        self.ignore = []#['waypoint-reached']

    def handle(self, signal, sender, data = None, time = 0):

        if(signal in self.ignore):
            return 0

        print '+----------------------------------------------+'
        print '| Time: %s units' % time
        print '| %s :: %s' % (sender.__class__.__name__, signal)
        print '| Data: %s' % data
        print '| %s' % sender
        print '+----------------------------------------------+'