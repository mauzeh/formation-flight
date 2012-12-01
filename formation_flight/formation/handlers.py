"""Handlers listen and react to events."""

from lib import sim
from allocators import * 
from synchronizers import * 
from lib.debug import print_line as p
from lib.geo.segment import Segment
from lib.geo.util import project_segment, get_hookoff_quotient, midpoint
import config

"""Uses the aircraft-depart event to initiate formation allocation"""

allocator = FormationAllocatorEtah()
synchronizer = FormationSynchronizer()

def init():
    sim.dispatcher.register('aircraft-depart', handle_departure)
    sim.dispatcher.register('enter-lock-area', handle_lock)
    sim.dispatcher.register('formation-alive', handle_alive)

def handle_departure(event):
    """Adds the aircraft to the candidate stack and schedules lock event."""

    aircraft  = event.sender
    global allocator
    
    # Register which hub this aircraft will fly to
    aircraft.hub = aircraft.route.waypoints[0]
    
    allocator.add_aircraft(aircraft)        
    sim.events.append(sim.Event(
        'enter-lock-area',
        aircraft,
        # If aircraft departs from within lock area, set lock time to now
        sim.time + max(aircraft.time_to_waypoint() - config.lock_time, 0)
    ))

def handle_lock(event):
    """Upon lock, find a formation (if exists) for current aircraft."""

    aircraft  = event.sender
    global allocator
    
    # Find the formation having self.
    formation = allocator.find_formation(aircraft)

    # Never try to allocate again, even if no formation was found
    allocator.remove_aircraft(aircraft)

    # If no formation is possible
    if formation is None or not len(formation) > 1:
        p('No formation was possible: %s' % formation)
        return

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

    # Determine formation trunk route
    destinations = []
    for aircraft in formation:
        destinations.append(aircraft.destination)
    arrival_midpoint = midpoint(destinations)
    p('destinations: %s' % destinations)
    p('midpoint = %s' % arrival_midpoint)
    hub_to_midpoint = Segment(aircraft.hub, arrival_midpoint)

    # Determine hookoff point for each aircraft, except the last
    for aircraft in formation:
        
        hub_to_destination = Segment(aircraft.hub, aircraft.destination)
        
        p('flight %s hub %s to destination: %s' % (
            aircraft,
            '%s{%d, %d}' % (
                aircraft.hub,
                aircraft.hub.lat,
                aircraft.hub.lon
            ),
            aircraft.destination
        ))
        p('flight %s hub %s to midpoint: %s' % (
            aircraft,
            '%s{%d, %d}' % (
                aircraft.hub,
                aircraft.hub.lat,
                aircraft.hub.lon
            ),
            arrival_midpoint
        ))

        theta = abs(hub_to_destination.get_initial_bearing() -
                    hub_to_midpoint.get_initial_bearing())
        (a, b) = project_segment(theta, hub_to_destination.get_length())
        aircraft.Q = get_hookoff_quotient(a, b, config.alpha)
        
        p('hookoff params for aircraft %s: %s' % (
            aircraft,
            'a = %s, b = %s, Q = %s' % (
                a, b, aircraft.Q
            )
        ))
        
        aircraft.hookoff_point = formation.hub.get_position(
            hub_to_midpoint.get_initial_bearing(),
            a * aircraft.Q
        )
        hub_to_hookoff = Segment(aircraft.hub, aircraft.hookoff_point)
        
        p('flight %s, hub %s to hook-off point: %s' % (
            aircraft,
            '%s{%d, %d}' % (
                aircraft.hub,
                aircraft.hub.lat,
                aircraft.hub.lon
            ),
            aircraft.hookoff_point
        ))

        # If Z is really big, the hookoff point may inadvertedly be
        # projected back into where the aircraft came from. In that case,
        # there is no benefit to flying in formation so the aircraft should
        # hook off as soon as they hook up.
        #angle = hub_to_destination.get_initial_bearing() -\
        #        hub_to_hookoff.get_initial_bearing()
        #p('angle = %s - %s = %s' % (
        #    hub_to_destination.get_initial_bearing(),
        #    hub_to_hookoff.get_initial_bearing(),
        #    angle
        #))
        #if abs(angle) > 90:
        #    aircraft.hookoff_point = aircraft.hub
        #    hub_to_hookoff = Segment(aircraft.hub, aircraft.hookoff_point)

        aircraft.hookoff_point.name = 'hookoff-%s' % aircraft.hookoff_point
        aircraft.P = hub_to_hookoff.get_length() / hub_to_midpoint.get_length()
        
    # Place aircraft in order, ascending with Q, to fulfill LIFO condition.
    formation = sorted(formation, key = lambda item: item.P)
    
    # All aircraft at the front of the formation having the same destination
    # should hook off where the previous buddy (having a different
    # destination) hooked off.
    
    # Example: formation AMS-SFO, BRU-SFO, LHR-ATL.
    # AMS-SFO and BRU-SFO should hook off where LHR-ATL hooked off.
    
    # First find the leading set of aircraft having the same destination
    formation.reverse()
    leading_destination = formation[0].destination
    leaders = []
    for aircraft in formation:
        if not aircraft.destination.coincides(leading_destination):
            break
        leaders.append(aircraft)
    
    p('Leaders of formation %s are %s' % (
        formation,
        leaders
    ))
    
    # Then find the buddy just before the set of leading aircraft, if
    # it exists.
    try:
        # The leaders: same hookoff point as last buddy.
        last_buddy = formation[len(leaders)]
        for aircraft in leaders:
            aircraft.Q = last_buddy.Q
            aircraft.P = last_buddy.P
            aircraft.hookoff_point = last_buddy.hookoff_point
    except IndexError:
        pass

    #assert 0

    # Change reversed formation back to normal
    formation.reverse()
    
    #debug.print_object(aircraft)
    #assert aircraft.waypoints_passed[1].coincides(aircraft.hub)
    
    for aircraft in formation:

            p('Adjusting waypoints of %s. Initial waypoints: %s' % (
                aircraft,
                aircraft.route.waypoints
            ))
            aircraft.route.waypoints = [
                #aircraft.hub,
                aircraft.hookoff_point,
                aircraft.destination]
            aircraft.route.init_segments()
            p('Adjusted waypoints of %s. New waypoints: %s' % (
                aircraft,
                aircraft.route.waypoints
            ))
            p('Need to calibrate aircraft %s (%s) in formation %s' % (
                aircraft, aircraft.route, formation
            ))
            aircraft.controller.calibrate()