from formation_flight.aircraft import Aircraft
from formation_flight.formation import Formation
from formation_flight.geo.waypoint import Waypoint

if __name__ == '__main__':

    point = Waypoint('AMS')
    print point.distance_to(Waypoint('FRA'))
    print point.distance_to(Waypoint('CDG'))
    print point.distance_to(Waypoint('BRU'))
    print point.distance_to(Waypoint('ZRH'))

    aircraft1 = Aircraft("AF")
    aircraft1.speed = 1
    aircraft1.departure_time = 0
    aircraft1.waypoints = [Waypoint('CDG'),
                           Waypoint('AMS'),
                           Waypoint('JFK'),
                           Waypoint('ORD')]

    aircraft2 = Aircraft("LH")
    aircraft2.departure_time = 0
    aircraft2.waypoints = [Waypoint('FRA'),
                           Waypoint('AMS'),
                           Waypoint('JFK'),
                           Waypoint('ORD')]

    formation = Formation()
    formation.route = [Waypoint('AMS'), Waypoint('JFK')]
    formation.start_time = 0