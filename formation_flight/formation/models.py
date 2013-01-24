"""Models contain information and do not initiate actions or commands.""" 

from lib import sim
from allocators import * 
from synchronizers import * 
from lib.debug import print_line as p
from lib.geo.segment import Segment
#from lib.geo.util import project_segment, get_hookoff_quotient
from lib.geo.util import midpoint
from lib.geo.hookoff import get_hookoff
import config

class Formation(list):
    """A bundle of flights."""
    
    def get_debug_lines(self):
        """Customize debug output"""
        lines = []
        for aircraft in self:
            lines.append(('%s' % aircraft, aircraft.description))
        return lines
    
    def calibrate(self):
        """Determines the trunk route and hookoff points"""
        
        # Determine formation trunk route
        destinations = []
        for aircraft in self:
            destinations.append(aircraft.destination)
        arrival_midpoint = midpoint(destinations)
        p('destinations: %s' % destinations)
        p('midpoint = %s' % arrival_midpoint)
        hub_to_midpoint = Segment(aircraft.hub, arrival_midpoint)
    
        # Determine hookoff point for each aircraft, except the last
        for aircraft in self:
            
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
    
            #theta = abs(hub_to_destination.get_initial_bearing() -
            #            hub_to_midpoint.get_initial_bearing())
            #(a, b) = project_segment(theta, hub_to_destination.get_length())
            #aircraft.Q = get_hookoff_quotient(a, b, config.alpha)

            #p('critical', 'hookoff params for aircraft %s: %s' % (
            #    aircraft,
            #    'a = %s, b = %s, Q = %s, HUB to HOOKOFF = %.2f' % (
            #        a, b, aircraft.Q, a * aircraft.Q
            #    )
            #))

            #aircraft.hookoff_point = self.hub.get_position(
            #    hub_to_midpoint.get_initial_bearing(),
            #    a * aircraft.Q
            #)
            
            aircraft.hookoff_point = get_hookoff(
                hub_to_midpoint,
                aircraft.destination,
                config.alpha
            )
            
            hub_to_hookoff = Segment(aircraft.hub, aircraft.hookoff_point)
            
            aircraft.Q = hub_to_hookoff.get_length() /\
                         hub_to_midpoint.get_length()

            p('flight %s, hub %s to hook-off point: %s' % (
                aircraft,
                '%s{%d, %d}' % (
                    aircraft.hub,
                    aircraft.hub.lat,
                    aircraft.hub.lon
                ),
                aircraft.hookoff_point
            ))
    
            aircraft.hookoff_point.name = 'hookoff-%s' % aircraft.hookoff_point
            
        # Place aircraft in order, ascending with Q, to fulfill LIFO condition.
        formation = sorted(self, key = lambda item: item.Q)
    
        # All aircraft at the front of the formation having the same destination
        # should hook off where the previous buddy (having a different
        # destination) hooked off.
    
        # Example: formation AMS-SFO, BRU-SFO, LHR-ATL.
        # AMS-SFO and BRU-SFO should hook off where LHR-ATL hooked off.
        # @todo Let AMS-SFO and BRU-SFO continue together along a new average
        #       formation trajectory (in this case directly to the destination)
    
        # First find the leading set of aircraft having the same destination
        formation.reverse()
        leading_destination = formation[0].destination
        leaders = []
        for aircraft in formation:
            
            # Start with always incurring benefits
            aircraft.incurs_benefits = True
    
            if not aircraft.destination.coincides(leading_destination):
                aircraft.is_leader = False
                continue

            aircraft.is_leader = True
            
            # Only the first leader incurs no benefits at all
            if len(leaders) == 0:
                aircraft.incurs_benefits = False
            
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
                #aircraft.P = last_buddy.P
                aircraft.hookoff_point = last_buddy.hookoff_point
        except IndexError:
            pass
    
        # Change reversed formation back to normal
        formation.reverse()

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