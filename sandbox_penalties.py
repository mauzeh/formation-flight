from formation_flight.geo import util
from formation_flight.geo.segment import Segment
from formation_flight.geo.point import Point
from formation_flight.geo.waypoint import Waypoint
from formation_flight.geo.route import Route
from formation_flight.aircraft import Aircraft
from formation_flight import simulator
from formation_flight import config

fuel_burn_per_nm   = .88
formation_discount = .13
v_opt              = 250
    
def penalty(aircraft, departure_hub, arrival_hub, etdh):

    origin      = aircraft.route.waypoints[0]
    destination = aircraft.route.waypoints[-1]
    position    = aircraft.get_position()

    direct_length    = aircraft.route.get_length()
    departure_length = origin.distance_to(position) +\
                       position.distance_to(departure_hub)
    formation_length = departure_hub.distance_to(arrival_hub)
    arrival_length   = arrival_hub.distance_to(destination)

    direct_costs = direct_length * fuel_burn_per_nm
    formation_costs = fuel_burn_per_nm * (departure_length + arrival_length) +\
                      fuel_burn_per_nm * (1 - formation_discount) *\
                      formation_length
    print 'Fuel burn if flying direct, solo: %.2f' % direct_costs
    print 'Fuel burn if flying in formation: %.2f' % formation_costs

    # Temporarily insert the hubs into the aircraft's route
    old_waypoints                = aircraft.route.waypoints
    aircraft.route.waypoints = [aircraft.route.waypoints[0],
                                position,
                                departure_hub,
                                arrival_hub,
                                aircraft.route.waypoints[-1]]

    print aircraft#.route.waypoints

    # Change route back to what it was
    aircraft.route.waypoints = old_waypoints
    print aircraft
    pass

def speed_penalty(v):

    return 1 + abs(v - v_opt) / v_opt 
    
if __name__ == '__main__':

    planes = [
        Aircraft(route = Route([Waypoint('AMS'), Waypoint('JFK')]))
    ]

    simulator.execute([10], planes);
    
    departure_hub = Waypoint('LHR')
    arrival_hub   = Waypoint('BOS')

    penalty(planes[0], departure_hub, arrival_hub, 10)