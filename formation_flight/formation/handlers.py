"""Handlers listen and react to events."""

from lib import sim
from allocators import * 
from synchronizers import * 
from lib.debug import print_line as p
import config

"""Uses the aircraft-depart event to initiate formation allocation"""

allocator = FormationAllocatorEtah()
synchronizer = FormationSynchronizer()

def init():
    sim.dispatcher.register('aircraft-depart', handle_departure)
    sim.dispatcher.register('enter-lock-area', handle_lock)
    sim.dispatcher.register('aircraft-at-waypoint', handle_waypoint)
    sim.dispatcher.register('formation-alive', handle_alive)

def handle_departure(event):
    """Adds the aircraft to the candidate stack and schedules lock event."""

    aircraft  = event.sender
    global allocator
    
    # Register which hub this aircraft will fly to
    aircraft.hub = aircraft.route.waypoints[0]
    
    assert aircraft.time_to_waypoint() > config.lock_time
    
    # If the origin lies within the hub lock area, the aircraft cannot
    # reach cruise before reaching the hub, so instead we ignore it altogether
    # and tell it to fly directly to its destination instead of via the hub.
    #if(aircraft.time_to_waypoint() < config.lock_time):
    #    
    #    # Reset the aircraft route
    #    aircraft.route.waypoints = [
    #        aircraft.position,
    #        aircraft.destination
    #    ]
    #    aircraft.route.init_segments()
    #    aircraft.controller.calibrate()
    #    p('debug', (
    #        '++++++++++++++++++++++++++Aircraft %s not participating in formation flight due to the ' +
    #        'origin being within the lock area' % (
    #            aircraft
    #        )
    #    ))
    #    return

    allocator.add_aircraft(aircraft)        
    sim.events.append(sim.Event(
        'enter-lock-area',
        aircraft,
        # If aircraft departs from within lock area, set lock time to now
        sim.time + max(aircraft.time_to_waypoint() - config.lock_time, 0)
    ))

def handle_waypoint(event):
    # Aircraft is no longer a candidate when it arrives at any waypoint
    # @todo Only remove from queue if at hub. But it's unlikely that aircraft
    # reach another waypoint before the hub so this is fine for now.
    p('Aircraft %s at waypoint, no longer formation candidate' % event.sender)
    allocator.remove_aircraft(event.sender)

def handle_lock(event):
    """Upon lock, find a formation (if exists) for current aircraft."""

    aircraft = event.sender
    global allocator
    
    # Find the formation having self.
    formation = allocator.find_formation(aircraft)

    # If no formation is possible
    if formation is None or not len(formation) > 1:
        p('No formation was possible: %s' % formation)
        return

    # If a formation was found, aircraft is no longer a candidate
    allocator.remove_aircraft(aircraft)

    # Register which hub this formation belongs to
    formation.hub = formation[0].hub

    p('Formation init: %s' % formation)

    # Remove 'enter-lock-area' events for all buddies
    sim.events = filter(lambda e: e.label != 'enter-lock-area' or
                                  e.sender not in formation, sim.events)

    # Prevent buddies from being allocated somewhere else.
    for buddy in formation:
        # Self was already removed
        if buddy is not aircraft:
            allocator.remove_aircraft(buddy)

    global synchronizer
    synchronizer.synchronize(formation)

def handle_alive(event):
    """Initialize the formation and determine hookoff points."""

    formation = event.sender
    formation.calibrate()