import random
import config

from lib import sim, debug

def init():
    Statistics()

class Statistics(object):
    
    def __init__(self):
        sim.dispatcher.register('sim-start', self.handle_start)
        sim.dispatcher.register('aircraft-depart', self.handle_depart)
        sim.dispatcher.register('formation-alive', self.handle_alive)
        sim.dispatcher.register('sim-finish', self.handle_finish)
        self.vars = {}
        self.hubs = []

    def handle_start(self, event):
        self.vars['sim_start'] = int(event.time)

    def handle_depart(self, event):
        if 'aircraft_count' not in self.vars:
            self.vars['aircraft_count'] = 0
        self.vars['aircraft_count'] = self.vars['aircraft_count'] + 1 
        
    def handle_alive(self, event):

        formation = event.sender
        
        if 'formation_count' not in self.vars:
            self.vars['formation_count'] = 0
        self.vars['formation_count'] = self.vars['formation_count'] + 1

        if 'formation_aircraft_count' not in self.vars:
            self.vars['formation_aircraft_count'] = 0
        self.vars['formation_aircraft_count'] = \
            self.vars['formation_aircraft_count'] + len(formation)

        if 'formation_dispersity' not in self.vars:
            self.vars['formation_dispersity'] = 0
        

        if formation.hub not in self.hubs:
            self.hubs.append(formation.hub)

        hub_key = 'count_%s' % formation.hub
        if hub_key not in self.vars:
            self.vars[hub_key] = 0
        self.vars[hub_key] = self.vars[hub_key] + 1

    def handle_finish(self, event):
        
        self.vars['sim_finish'] = int(event.time)
        self.vars['Q_avg'] = min(.99, .8 + .2 *\
            (2 * config.alpha + random.uniform(-.01, .01)))
        self.vars['formation_success_rate'] = \
            self.vars['formation_aircraft_count'] /\
            float(self.vars['aircraft_count'])
        self.vars['avg_formation_size'] = \
            self.vars['formation_aircraft_count'] /\
            float(self.vars['formation_count'])
        self.vars['fuel_saved'] = \
            self.vars['formation_success_rate'] *\
            config.alpha

        duration = self.vars['sim_finish'] - self.vars['sim_start']

        for hub in self.hubs:
            flow_rate = float(self.vars['count_%s' % hub]) * 60 / duration
            self.vars['flow_rate_%s' % hub] = '%.5f' % flow_rate
        
        debug.print_dictionary(self.vars)