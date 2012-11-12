"""Captures data and puts it into data/output.tsv"""
import csv, sim

class Sink(object):

    def put(self, row = []):
        assert isinstance(row, list)
        self.writer.writerow(row)

class AircraftSink(Sink):

    def __init__(self):
        self.writer = csv.writer(open('data/output_aircraft.tsv', 'w'), delimiter = '\t')
        sim.dispatcher.register('aircraft-arrive', self.handle_arrival)

    def handle_arrival(self, event):
        
        aircraft = event.sender

        try:
            formation = aircraft.formation
            formation_id = formation.id
        # Not all aircraft end up in formations
        except AttributeError:
            formation_id = 0

        self.put([
            '% 4d' % event.time,
            '% 6s' % aircraft.label,
            '% 4d' % aircraft.departure_time,
            '%s'   % aircraft.description,
            '% 4d' % formation_id,
            '% 4d' % aircraft.route.get_length()
        ])
        
class FormationSink(Sink):

    def __init__(self):
        self.writer = csv.writer(open('data/output_formation.tsv', 'w'), delimiter = '\t')
        self.attrs = {}
        sim.dispatcher.register('formation-alive', self.handle_alive)

    def handle_alive(self, event):
        
        # @todo do we need this? maybe remove?
        # @todo move to class similar to statistics.py?
        # Create a formation id to be used in the data sink.
        if not 'formation_count' in self.attrs:
            self.attrs['formation_count'] = 0
        self.attrs['formation_count'] = self.attrs['formation_count'] + 1
        formation = event.sender
        formation.id = self.attrs['formation_count']

        # Tell aircraft in which formation it is flying.
        # @todo move to class similar to statistics.py?
        for aircraft in formation:
            aircraft.formation = formation
        
        formation = event.sender

        self.put([
            '%s'   % formation.id,
            '%04d' % event.time,
            '% 3s' % formation.hub,
            '%02d' % len(formation),
        ])
        
def init():
    AircraftSink()
    FormationSink()