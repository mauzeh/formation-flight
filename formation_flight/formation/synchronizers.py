"""Synchronizers schedule formation hook-ups by changing the aircraft speed.

Makes sure that each participant arrives at the right time."""

from lib import sim, debug
from lib.debug import print_line as p
import random
import config

class FormationSynchronizer(object):
    
    def synchronize(self, formation):

        # @todo Rationalize and remodel.
        leader = formation[0]
        leader.controller.update_position()
        time_to_hub = leader.time_to_waypoint()

        # Happens when origin is very close to hub
        if time_to_hub < config.etah_slack:
            p('Ignore: hub is too close to formation leader origin.')
            return
        
        for aircraft in formation:

            # Make sure the position of the aircraft is current
            aircraft.controller.update_position()

            # Adjust the speed of the aircraft
            ratio = aircraft.time_to_waypoint() / float(time_to_hub)

            # Unrealistic speeds = modeling error!
            if not (ratio < 2 and ratio > 0.5):
                debug.print_object(formation)
                debug.print_object(aircraft)
                continue
                #raise Exception('haha')

            aircraft.speed = aircraft.speed * ratio

            # Replan all events.
            aircraft.controller.calibrate()

        sim.events.append(sim.Event(
            'formation-alive',
            formation,
            # Add a tiny delay to make sure that all aircraft-at-waypoint
            # events are fired before the formation-alive event.
            sim.time + time_to_hub + 0.0001
        ))