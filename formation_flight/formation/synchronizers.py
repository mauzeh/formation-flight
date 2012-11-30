"""Synchronizers schedule formation hook-ups by changing the aircraft speed.

Makes sure that each participant arrives at the right time."""

from lib import sim, debug
from lib.debug import print_line as p
import random
import config

class FormationSynchronizer(object):
    
    def synchronize(self, formation):
        
        for aircraft in formation:
            
            # Ensure position is up-to-date for eta calculation later
            aircraft.controller.update_position()
            
            # Ensure all participants have the hub as their active waypoint
            assert aircraft.route.waypoints[0].coincides(formation.hub)

        # Select the aircraft that arrives last at the hub
        last_aircraft = max(formation, key = lambda a: a.time_to_waypoint())
        time_to_hub   = last_aircraft.time_to_waypoint()
        
        p('The last aircraft in formation %s is: %s.' % (
            formation, last_aircraft
        ))
        p('The time to hub for formation %s is %d.' % (
            formation, time_to_hub
        ))

        for aircraft in formation:
            
            if aircraft is last_aircraft:
                continue
            
            # Make sure the position of the aircraft is current
            aircraft.controller.update_position()
            
            # Compute time difference between arrivals
            delay = time_to_hub - aircraft.time_to_waypoint()
            
            p('Original hub arrival time for aircraft %s: %d.' % (
                aircraft, sim.time + aircraft.time_to_waypoint()
            ))
            
            p('Required hub arrival time for aircraft %s: %d.' % (
                aircraft, sim.time + time_to_hub
            ))
            
            p('Required hub arrival delay for aircraft %s: %d.' % (
                aircraft, delay
            ))

            # We should only delay, never expedite
            assert delay >= 0

            # Delay arrival of participant to match required arrival.
            aircraft.controller.delay_events(delay)

        # Add a tiny delay to make sure that all aircraft-at-waypoint
        # events are fired before the formation-alive event.
        formation_alive_time = sim.time + time_to_hub + 0.0001
        p('Set formation-alive time at %d + %d = %d for formation %s' % (
            sim.time,
            time_to_hub,
            formation_alive_time,
            formation
        ))
        sim.events.append(sim.Event(
            'formation-alive',
            formation,
            formation_alive_time
        ))