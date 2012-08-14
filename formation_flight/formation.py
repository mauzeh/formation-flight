from pydispatch import dispatcher
from formation_flight.aircraft import Aircraft
from formation_flight.geo.waypoint import Waypoint
from lib.intervals import Interval, group
from formation_flight import simulator, config

class Formation(object):
    """Represents a group of aircraft flying together"""

    def __init__(self, aircraft = []):

        assert len(aircraft) > 0

        self.aircraft = aircraft

        # Statuses:
        # pending - Not flying yet, open to receive aircraft
        # locked - Not flying yet, not open to receive aircraft
        # active  - Flying. Not open to receive aircraft
        self.status = 'pending'

        # The time at which the formation is set to start
        self.start_time = 0

    def get_start_eta(self):
        """Calculates when the formation is set to start"""

        # for now, delay all early participants
        # ETA equals eta of first participant
        return self.aircraft[0].get_waypoint_eta()

    def synchronize(self):
        """Aligns the arrival times of all aircraft into the hub."""

        start_eta = self.get_start_eta()
        formation_time_to_hub = self.get_start_eta() - simulator.get_time()
        for aircraft in self.aircraft:
            aircraft_time_to_hub  = aircraft.get_waypoint_eta() - simulator.get_time()
            aircraft.speed = aircraft.speed * aircraft_time_to_hub / formation_time_to_hub

    def lock(self):
        self.status = 'locked'

        # Synchronize all aircraft to arrive at the same time
        self.synchronize()

        dispatcher.send(
            'formation-locked',
            time = simulator.get_time(),
            sender = self,
            data = self
        )

    def __repr__(self):
        return '%s' % self.aircraft

class Assigner(object):
    """Perform aircraft formation assignment by hooking in to certain simulation events."""

    def __init__(self):

        # List of aircraft that have not been assigned to a formation
        self.aircraft_queue = []

        # List of assigned formations (each containing assigned aircraft)
        # this list is repopulated each time the aircraft queue changes
        self.pending_formations = []

        # List of locked formations. Nothing can be done to change these
        self.locked_formations = []
        dispatcher.connect(self.register_takeoff, 'takeoff')
        dispatcher.connect(self.try_to_lock_formations, 'fly')
        dispatcher.connect(self.synchronize, 'formation-lock')

    def register_takeoff(self, signal, sender, data = None, time = 0):
        """Assign departing aircraft into pending or new formations."""

        assert type(sender) == Aircraft
        self.aircraft_queue.append(sender)
        self.assign()

    def assign(self):

        # how much time the arrival at the virtual hub can be delayed/expedited
        slack = config.virtual_hub_arrival_slack
        self.pending_formations = []

        for hub_name in config.virtual_hubs:

            # Create formations from the queuing aircraft
            hub = Waypoint('AMS')
            candidates = []
            aircraft_by_name = {}

            for aircraft in self.aircraft_queue:

                if aircraft.get_current_waypoint().name != hub_name:
                    continue

                aircraft_by_name[aircraft.name] = aircraft

                hub_eta = aircraft.get_waypoint_eta()
                candidates.append(
                    Interval(aircraft.name,
                             int(hub_eta - slack),
                             int(hub_eta + slack)))

            for interval_group in group(candidates):
                aircraft_list = []
                for interval in interval_group:
                    aircraft_list.append(aircraft_by_name[interval.name])
                formation = Formation(aircraft_list)
                self.pending_formations.append(Formation(aircraft_list))
                dispatcher.send(
                    'formation-init',
                    time = simulator.get_time(),
                    sender = self,
                    data = formation
                )

    def try_to_lock_formations(self, signal, sender, data, time):

        if len(self.pending_formations) <= 0: return

        for formation in self.pending_formations:

            # if formation ETA is less than 10 time units away, lock it
            if formation.get_start_eta() - simulator.get_time() <= 10:
                # remove participants from aircraft queue
                self.remove_from_queue(formation)
                formation.lock()


    def remove_from_queue(self, formation):
        assert type(formation) == Formation
        if not len(self.aircraft_queue) > 0: return

        for aircraft in formation.aircraft:
            for q_a in self.aircraft_queue:
                if q_a.name == aircraft.name:
                    self.aircraft_queue.remove(q_a)
        self.assign()

    def synchronize(self, signal, sender, data = None, time = 0):
        """Makes sure that all aircraft in a formation arrive simultaneously"""
        assert type(data) == Formation

        # distance to virtual hub

        # set speed so that arrival @ hub = 80 units
        #time_to_hub = 79.9999 - time
        #sender.speed = distance / time_to_hub
