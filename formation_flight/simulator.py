class Simulator(object):

    def __init__(self):
        self.time = range(0, 60*60, 1)
        self.aircraft_list = []

    def execute(self):

        for t in self.time:
            for plane in self.aircraft_list:
                pos = plane.get_position(t)
                if(pos == 0):
                    self.aircraft_list.remove(plane)
            else:
                continue
            #break
