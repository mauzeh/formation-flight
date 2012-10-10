import random

class FormationSynchronizer(object):
    def synchronize(self, formation):
        """Makes sure that each participant arrives at the right time."""

        # @todo Rationalize and remodel.
        leader = formation[0]
        leader.controller.update_position()
        time_to_hub = leader.time_to_waypoint()
        for aircraft in formation:

            # Make sure the position of the aircraft is current
            aircraft.controller.update_position()

            # Adjust the speed of the aircraft
            ratio = aircraft.time_to_waypoint() / time_to_hub
            aircraft.speed = aircraft.speed * ratio

            # Replan all events.
            aircraft.controller.calibrate()
