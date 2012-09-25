from pydispatch import dispatcher
from formation_flight.aircraft import Aircraft
from formation_flight.geo.waypoint import Waypoint
from lib.intervals import Interval, group
from formation_flight import simulator, config

def register():
    dispatcher.connect(handle)

def handle(signal, sender, data = None, time = 0):

    if not hasattr(handle, "assigner"):
        handle.assigner = Assigner()

    if signal is 'fly':
        handle.assigner.lock_formations()
    if signal is 'takeoff':
        handle.assigner.register_takeoff(aircraft = sender)
    
class Formation(object):
    """Represents a group of aircraft flying together.

    Introduces and fires a new event: "formation-locked"."""

    def __init__(self, aircraft = []):

        assert len(aircraft) > 0

        self.aircraft = aircraft

        # Statuses:
        # pending - Not flying yet. Open to receive aircraft
        # locked  - Not flying yet. Not open to receive aircraft
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
            waypoint_eta = aircraft.get_waypoint_eta()
            time_to_hub  = waypoint_eta - simulator.get_time()
            speed = aircraft.speed
            aircraft.speed = speed * time_to_hub / formation_time_to_hub

    def lock(self):
        """Locks this formation. It can no longer accept aircraft"""
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
    """Assigns aircraft into formations"""

    def __init__(self):

        # List of aircraft that have not been assigned to a formation
        self.aircraft_queue = []

        # List of assigned formations (each containing assigned aircraft)
        # this list is repopulated each time the aircraft queue changes
        self.pending_formations = []

        # List of locked formations. Nothing can be done to change these
        self.locked_formations = []

    def register_takeoff(self, aircraft):
        """Registers departing aircraft, and assigns into formations."""

        assert type(aircraft) == Aircraft
        self.aircraft_queue.append(aircraft)
        self.assign()

    def assign(self):
        """Groups airborne aircraft having an ETAH overlap"""

        # how much time the arrival at the virtual hub can be delayed/expedited
        slack = config.virtual_hub_arrival_slack
        self.pending_formations = []

        for hub_name in config.virtual_hubs:

            # Create formations from the queuing aircraft.
            candidates = []

            for aircraft in self.aircraft_queue:

                # Disregard if not flying to hub under consideration.
                if aircraft.get_current_waypoint().name != hub_name:
                    continue

                hub_eta = aircraft.get_waypoint_eta()
                candidates.append(
                    Interval(aircraft,
                             int(hub_eta - slack),
                             int(hub_eta + slack)))

            for interval_group in group(candidates):
                aircraft_list = []
                for interval in interval_group:
                    aircraft_list.append(interval.obj)
                formation = Formation(aircraft_list)
                self.pending_formations.append(Formation(aircraft_list))
                dispatcher.send(
                    'formation-init',
                    time = simulator.get_time(),
                    sender = self,
                    data = formation
                )

    def lock_formations(self):
        """Locks pending formations if they are within range of the hub"""
        if len(self.pending_formations) <= 0: return

        for formation in self.pending_formations:

            # if formation ETA is less than 10 time units away, lock it
            time_remaining = formation.get_start_eta() - simulator.get_time()
            lock_time = config.formation_lock_time
            if time_remaining <= lock_time:
                # remove participants from aircraft queue
                self.remove_from_queue(formation)
                formation.lock()

    def remove_from_queue(self, formation):
        """Removes aircraft that are locked into formations from the queue"""
        assert type(formation) == Formation
        if not len(self.aircraft_queue) > 0: return

        for aircraft in formation.aircraft:
            for q_a in self.aircraft_queue:
                if q_a.name == aircraft.name:
                    print 'Removing %s from queue' % q_a
                    self.aircraft_queue.remove(q_a)
        # @todo is this really necessary? wasn't this triggered by assign
        # in the first place?
        self.assign()
