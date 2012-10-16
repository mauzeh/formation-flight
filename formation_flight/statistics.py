from lib import sim, debug

def init():
    Statistics()

class Statistics(object):
    
    def __init__(self):
        sim.dispatcher.register('sim-start', self.handle_start)
        sim.dispatcher.register('formation-alive', self.handle_alive)
        sim.dispatcher.register('sim-finish', self.handle_finish)
        self.vars = {}
        self.hubs = []

    def handle_start(self, event):
        self.vars['sim_start'] = int(event.time)
        
    def handle_alive(self, event):

        formation = event.sender
        
        if 'formation_count' not in self.vars:
            self.vars['formation_count'] = 0
        self.vars['formation_count'] = self.vars['formation_count'] + 1

        if formation.hub not in self.hubs:
            self.hubs.append(formation.hub)

        hub_key = 'count_%s' % formation.hub
        if hub_key not in self.vars:
            self.vars[hub_key] = 0
        self.vars[hub_key] = self.vars[hub_key] + 1

    def handle_finish(self, event):
        
        self.vars['sim_finish'] = int(event.time)

        duration = self.vars['sim_finish'] - self.vars['sim_start']

        for hub in self.hubs:
            flow_rate = float(self.vars['count_%s' % hub]) * 60 / duration
            self.vars['flow_rate_%s' % hub] = '%.5f' % flow_rate
        
        debug.print_dictionary(self.vars)