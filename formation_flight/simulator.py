from pydispatch import dispatcher

class Simulator(object):

    def __init__(self):
        self.time = range(0, 60*60, 1)
        self.aircraft = []

    def execute(self):

        dispatcher.send(
            'sim-init',
            sender = self,
            time = 0,
            data = 'Initializing simulation'
        )

        for t in self.time:
            for plane in self.aircraft:
                pos = plane.get_position(t)
                if(pos == 0):
                    self.aircraft.remove(plane)
            else:
                continue
            #break
