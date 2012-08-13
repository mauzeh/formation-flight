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

    def get_start_time(self):
        """Calculates when the formation is set to start"""

        # for now, delay all early participants
        # ETA equals eta of first participant
        return self.aircraft[0].get_waypoint_eta()

    def synchronize(self):
        """Aligns the arrival times of all aircraft into the hub."""

        formation_time_to_hub = self.get_start_time() - simulator.get_time()
        for aircraft in self.aircraft:
            aircraft_time_to_hub  = aircraft.get_waypoint_eta() - simulator.get_time()
            aircraft.speed = aircraft.speed * aircraft_time_to_hub / formation_time_to_hub
            dispatcher.send(
                'aircraft-synchronize',
                time = simulator.get_time(),
                sender = self,
                data = aircraft
            )

    def lock(self):
        self.status = 'locked'
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
        ams = Waypoint('AMS')
        ein = Waypoint('EIN')
        self.aircraft_queue = {
            ams : [],
            ein : []
        }

        # List of assigned formations (each containing assigned aircraft)
        # this list is repopulated each time the aircraft queue changes
        self.pending_formations = []

        # List of locked formations. Nothing can be done to change these
        self.locked_formations = []

        dispatcher.connect(self.register_takeoff, 'takeoff')
        dispatcher.connect(self.lock_formations, 'fly')

    def register_takeoff(self, signal, sender, data = None, time = 0):
        """Assign departing aircraft into pending or new formations."""

        assert type(sender) == Aircraft
        sender_hub = sender.get_current_waypoint()
        self.aircraft_queue[sender_hub].append(sender)
        self.init_formations()

    def init_formations(self):

        slack = config.virtual_hub_arrival_slack
        self.pending_formations = []

        for hub, queue in self.aircraft_queue.items():

            # Create formations from the queuing aircraft
            candidates = []
            aircraft_by_name = {}
            for aircraft in queue:

                aircraft_by_name[aircraft.name] = aircraft

                # determine the ETA at the virtual hub
                hub_eta = simulator.get_time() + aircraft.get_position().distance_to(hub) / aircraft.speed
                candidates.append(Interval(aircraft.name, int(hub_eta - slack), int(hub_eta + slack)))

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

    def lock_formations(self, signal, sender, data, time):

        if len(self.pending_formations) <= 0: return

        for formation in self.pending_formations:

            # if formation ETA is less than 10 time units away, lock it
            if formation.get_start_time() - simulator.get_time() <= 10:
                formation.lock()
                self.locked_formations.append(formation)
                self.remove_from_queue(formation)

        dispatcher.send(
            'assigner-lock-formations',
            time = time,
            sender = self,
            data = self
        )


    def remove_from_queue(self, formation):
        """Removes all aircraft from said formation from the queue"""

        assert formation.status is not 'pending'
        assert type(formation) == Formation
        if not len(self.aircraft_queue) > 0: return

        for aircraft in formation.aircraft:

            self.aircraft_queue.remove(aircraft)

        self.init_formations()