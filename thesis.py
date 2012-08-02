from formation_flight.aircraft import Aircraft
from formation_flight.formation import Assigner
from formation_flight.simulator import Simulator
from formation_flight.waypoint import Waypoint
#from lib.events import EventHandler

if __name__ == '__main__':

#    handler = EventHandler()
    assigner = Assigner()

    sim = Simulator()
    sim.time = range(0, 120, 1)

    aircraft = Aircraft("AF65 330")
    aircraft.departure_time = 0
    aircraft.waypoints = [Waypoint('CDG'),
                           Waypoint('AMS'),
                           Waypoint('JFK')]
    sim.aircraft.append(aircraft)

    aircraft = Aircraft("LH23 744")
    aircraft.departure_time = 0
    aircraft.waypoints = [Waypoint('FRA'),
                           Waypoint('AMS'),
                           Waypoint('ORD')]
    sim.aircraft.append(aircraft)

    aircraft = Aircraft("SN23 744")
    aircraft.departure_time = 0
    aircraft.waypoints = [Waypoint('BRU'),
                          Waypoint('AMS'),
                          Waypoint('ORD')]
    sim.aircraft.append(aircraft)

    aircraft = Aircraft("LX23 744")
    aircraft.departure_time = 90
    aircraft.waypoints = [Waypoint('ZRH'),
                          Waypoint('AMS'),
                          Waypoint('ORD')]
    sim.aircraft.append(aircraft)

    sim.execute()

    # docs: http://docs.python.org/library/profile.html
#import cProfile, pstats
#profile_file = 'data/profile.txt'
#cProfile.run('run()', profile_file)
#p = pstats.Stats(profile_file)
#p.strip_dirs()
#p.sort_stats('cumulative')
#p.print_stats(15)