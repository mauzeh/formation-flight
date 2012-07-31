from formation_flight.aircraft import Aircraft
from formation_flight.formation import Assigner
from formation_flight.simulator import Simulator
from formation_flight.waypoint import Waypoint
#from lib.events import EventHandler

if __name__ == '__main__':

#    handler = EventHandler()
    assigner = Assigner()

    sim = Simulator()
    sim.time = range(0, 60*60*18, 60)

    aircraft1 = Aircraft("AF65 330")
    aircraft1.departure_time = 0
    aircraft1.waypoints = [Waypoint('CDG'),
                           Waypoint('AMS'),
                           Waypoint('JFK')]
    sim.aircraft.append(aircraft1)

    aircraft2 = Aircraft("LH23 744")
    aircraft2.departure_time = 60*60
    aircraft2.waypoints = [Waypoint('FRA'),
                           Waypoint('AMS'),
                           Waypoint('ORD')]
    sim.aircraft.append(aircraft2)

    sim.execute()

    # docs: http://docs.python.org/library/profile.html
#import cProfile, pstats
#profile_file = 'data/profile.txt'
#cProfile.run('run()', profile_file)
#p = pstats.Stats(profile_file)
#p.strip_dirs()
#p.sort_stats('cumulative')
#p.print_stats(15)