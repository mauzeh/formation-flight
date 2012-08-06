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

    aircraft = Aircraft("CDG")
    aircraft.departure_time = 0
    aircraft.waypoints = [Waypoint('CDG'),
                           Waypoint('AMS'),
                           Waypoint('JFK')]
    sim.aircraft.append(aircraft)

    aircraft = Aircraft("FRA")
    aircraft.departure_time = 0
    aircraft.waypoints = [Waypoint('FRA'),
                           Waypoint('AMS'),
                           Waypoint('ORD')]
    sim.aircraft.append(aircraft)

    aircraft = Aircraft("BRU")
    aircraft.departure_time = 0
    aircraft.waypoints = [Waypoint('BRU'),
                          Waypoint('AMS'),
                          Waypoint('LHR'),
                          Waypoint('MCO')]
    sim.aircraft.append(aircraft)
    aircraft.get_position(0)
    aircraft.get_position(5)
    aircraft.get_position(10)
    aircraft.get_position(15)
    aircraft.get_position(15.5)
    aircraft.get_position(16)
    aircraft.get_position(17)
    aircraft.get_position(18)
    aircraft.get_position(19)

    aircraft = Aircraft("ZRH")
    aircraft.departure_time = 90
    aircraft.waypoints = [Waypoint('ZRH'),
                          Waypoint('AMS'),
                          Waypoint('ORD')]
    sim.aircraft.append(aircraft)

    #sim.execute()

    # docs: http://docs.python.org/library/profile.html
#import cProfile, pstats
#profile_file = 'data/profile.txt'
#cProfile.run('run()', profile_file)
#p = pstats.Stats(profile_file)
#p.strip_dirs()
#p.sort_stats('cumulative')
#p.print_stats(15)