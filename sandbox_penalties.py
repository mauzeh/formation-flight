from formation_flight.geo import util
from formation_flight.geo.segment import Segment
from formation_flight.geo.point import Point
from formation_flight.geo.waypoint import Waypoint
from formation_flight.geo.route import Route
from formation_flight.aircraft import Aircraft
from formation_flight import simulator
from formation_flight import config
from lib import debug

fuel_burn_per_nm   = .88
formation_discount = .13
v_opt              = 8.333
    
def fuel_diff(aircraft, departure_hub, arrival_hub, required_etah,
            verbose = True):

    origin      = aircraft.route.waypoints[0]
    destination = aircraft.route.waypoints[-1]
    position    = aircraft.get_position()

    direct_length      = aircraft.route.get_length()
    origin_to_here     = origin.distance_to(position)
    here_to_hub_length = position.distance_to(departure_hub) 
    formation_length   = departure_hub.distance_to(arrival_hub)
    arrival_length     = arrival_hub.distance_to(destination)

    # Temporarily insert the hubs into the aircraft's route
    old_waypoints                = aircraft.route.waypoints
    aircraft.route.waypoints = [aircraft.route.waypoints[0],
                                position,
                                departure_hub,
                                arrival_hub,
                                aircraft.route.waypoints[-1]]

    planned_etah = aircraft.get_waypoint_eta()
    t = simulator.get_time()
    v_factor = (planned_etah - t) / (required_etah - t)
    v_old = aircraft._speed
    v_new = v_factor * v_old
    v_penalty = speed_penalty(v_new)

    direct_costs = direct_length * fuel_burn_per_nm
    formation_costs = fuel_burn_per_nm * origin_to_here +\
                      v_penalty * fuel_burn_per_nm * here_to_hub_length +\
                      fuel_burn_per_nm * (1 - formation_discount) *\
                      formation_length +\
                      fuel_burn_per_nm * arrival_length

    # Change route back to what it was
    aircraft.route.waypoints = old_waypoints

    if verbose:

        headers = []
        headers.append(('Mijn header', 'uhuh'))
        
        messages = []
        messages.append(('Flight', aircraft))
        messages.append(('Departure hub', departure_hub))
        messages.append(('Arrival hub', arrival_hub))
        messages.append(('Time to hub (planned)', '%d time units' % (planned_etah - t)))
        messages.append(('Time to hub (required)', '%d time units' % (required_etah - t)))
        messages.append(('Current speed', '%.0f kts' % (v_old*60)))
        messages.append(('Required speed', '%.0f kts' % (v_new*60)))
        messages.append(('Sync fuel', '%.2f gallons' %
              (v_penalty * fuel_burn_per_nm * here_to_hub_length)))
        messages.append(('Fuel (solo flight)', '%.2f gallons' % direct_costs))
        messages.append(('Fuel (formation flight)', '%.2f gallons' % formation_costs))
        debug.print_table(messages = messages, headers = headers)

    return direct_costs - formation_costs 

def speed_penalty(v):

    return 1 + abs(v - v_opt) / v_opt 
    
if __name__ == '__main__':

    planes = [
        Aircraft(route = Route([Waypoint('AMS'), Waypoint('JFK')]))
    ]

    simulator.execute([10], planes);
    
    departure_hub = Waypoint('LHR')
    arrival_hub   = Waypoint('BOS')

    p = fuel_diff(planes[0], departure_hub, arrival_hub, 20, verbose = True)

    debug.print_table([('Net benefit', '%d gallons' % p)])