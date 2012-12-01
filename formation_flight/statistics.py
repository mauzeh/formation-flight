import random
import config

from lib.geo.segment import Segment

from lib import sim, debug
from lib.debug import print_line as p

def init():
    Statistics()

class Statistics(object):
    
    def __init__(self):
        sim.dispatcher.register('sim-start', self.handle_start)
        sim.dispatcher.register('aircraft-depart', self.handle_depart)
        sim.dispatcher.register('formation-alive', self.handle_alive)
        sim.dispatcher.register('aircraft-arrive', self.handle_arrive)
        sim.dispatcher.register('sim-finish', self.handle_finish)
        self.vars = {}
        self.hubs = []

    def handle_start(self, event):
        self.vars['sim_start'] = int(event.time)

    def handle_depart(self, event):

        aircraft = event.sender

        if 'aircraft_count' not in self.vars:
            self.vars['aircraft_count'] = 0
        self.vars['aircraft_count'] = self.vars['aircraft_count'] + 1
        
        # If a hub was planned
        hub = aircraft.route.waypoints[0]
        #assert hub.is_hub
        if True:
            if hub not in self.hubs:
                self.hubs.append(hub)
                self.vars['formation_count_%s' % hub] = 0

    def handle_alive(self, event):

        formation = event.sender
        
        # We should have a hookoff point for each participant, and it should be
        # the current segment
        for aircraft in formation:
            assert aircraft.hookoff_point
            # The remaining segment should be hookoff-destination
            #debug.print_object(aircraft)
            assert len(aircraft.route.segments) > 0
            
            #assert aircraft.route.segments[0].end.coincides(
            #    aircraft.hookoff_point
            #)
        
        if 'formation_count' not in self.vars:
            self.vars['formation_count'] = 0
        self.vars['formation_count'] = self.vars['formation_count'] + 1

        if 'formation_aircraft_count' not in self.vars:
            self.vars['formation_aircraft_count'] = 0
        self.vars['formation_aircraft_count'] = \
            self.vars['formation_aircraft_count'] + len(formation)
            
        for aircraft in formation:
            if 'Q_sum' not in self.vars:
                self.vars['Q_sum'] = 0
                self.vars['Q_count'] = 0
            self.vars['Q_sum']   = self.vars['Q_sum'] + aircraft.Q
            self.vars['Q_count'] = self.vars['Q_count'] + 1
        
        hub_key = 'formation_count_%s' % formation.hub
        if hub_key not in self.vars:
            self.vars[hub_key] = 0
        self.vars[hub_key] = self.vars[hub_key] + 1
        
    def handle_arrive(self, event):
        
        aircraft = event.sender
        hub = aircraft.hub
        
        assert hub in self.hubs

        aircraft = event.sender
        hub = aircraft.hub
        p('Flight %s arrives at hub %s' % (
            aircraft, hub
            ))
        assert hub in self.hubs
        key = 'flight_count_%s' % hub
        if key not in self.vars:
            self.vars[key] = 0
        self.vars[key] = self.vars[key] + 1

        if 'distance_formation' not in self.vars:
            self.vars['distance_formation'] = 0
        if 'distance_solo' not in self.vars:
            self.vars['distance_solo'] = 0
        if 'distance_direct' not in self.vars:
            self.vars['distance_direct'] = 0

        # Aircraft always fly solo to the hub
        segment = Segment(aircraft.origin, hub)
        origin_to_hub = segment.get_length()
        p('Distance origin_to_hub for %s is %dNM' % (
            aircraft,
            origin_to_hub
        ))
        self.vars['distance_solo'] = self.vars['distance_solo'] +\
            origin_to_hub
        
        # If in formation
        if hasattr(aircraft, 'formation'):
            
            segment = Segment(hub, aircraft.hookoff_point)
            hub_to_hookoff = segment.get_length()
            p('Distance hub_to_hookoff for %s is %dNM' % (
                aircraft,
                hub_to_hookoff
            ))
            self.vars['distance_formation'] = self.vars['distance_formation'] +\
                hub_to_hookoff

            segment = Segment(aircraft.hookoff_point, aircraft.destination)
            hookoff_to_destination = segment.get_length()
            p('Distance hookoff_to_destination for %s is %dNM' % (
                aircraft,
                hookoff_to_destination
            ))
            self.vars['distance_solo'] = self.vars['distance_solo'] +\
                hookoff_to_destination

            # Collect all hub delays
            # The calibration aircraft was never delayed
            if hasattr(aircraft, 'hub_delay'):
                if 'hub_delay_sum' not in self.vars:
                    self.vars['hub_delay_sum'] = 0
                self.vars['hub_delay_sum'] = self.vars['hub_delay_sum'] +\
                    aircraft.hub_delay

        # If fully solo
        else:
            
            segment = Segment(hub, aircraft.destination)
            hub_to_destination = segment.get_length()
            p('Distance hub_to_destination for %s is %dNM' % (
                aircraft,
                hub_to_destination
            ))
            self.vars['distance_solo'] = self.vars['distance_solo'] +\
                hub_to_destination
            
        # Also calculate the direct distance
        segment = Segment(aircraft.origin, aircraft.destination)
        direct = segment.get_length()
        p('Distance direct for %s is %dNM' % (
            aircraft,
            direct
        ))
        self.vars['distance_direct'] = self.vars['distance_direct'] + direct

    def handle_finish(self, event):

        self.vars['sim_finish'] = int(event.time)
        if 'Q_sum' in self.vars:
            self.vars['Q_avg'] = self.vars['Q_sum'] / self.vars['Q_count']
        if 'formation_aircraft_count' in self.vars:
            self.vars['formation_success_rate'] = \
                self.vars['formation_aircraft_count'] /\
                float(self.vars['aircraft_count'])
            self.vars['avg_formation_size'] = \
                self.vars['formation_aircraft_count'] /\
                float(self.vars['formation_count'])
            self.vars['distance_total'] = \
                self.vars['distance_formation'] + self.vars['distance_solo']
            self.vars['distance_success_rate'] = \
                self.vars['distance_formation'] / self.vars['distance_total']
            self.vars['distance_penalty'] = -1 + \
                self.vars['distance_total'] / self.vars['distance_direct']
            self.vars['alpha_effective'] =\
                config.alpha *\
                self.vars['distance_success_rate'] -\
                self.vars['distance_penalty']
            self.vars['distance_penalty'] = -1 + \
                self.vars['distance_total'] / self.vars['distance_direct']
            self.vars['hub_delay_normalized'] = self.vars['hub_delay_sum'] /\
                self.vars['aircraft_count']

        duration = self.vars['sim_finish'] - self.vars['sim_start']
        debug.print_dictionary(self.vars)