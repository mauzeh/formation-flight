from formation_flight.aircraft import Aircraft
from formation_flight.formation import Assigner
from formation_flight.geo.route import Route
from formation_flight.geo.waypoint import Waypoint
from formation_flight.simulator import Simulator
from lib.events import EventHandler

if __name__ == '__main__':

    handler = EventHandler()
    assigner = Assigner()

    sim = Simulator()
    sim.time = range(0, 90, 1)

    route = Route([Waypoint('CDG'),
                   Waypoint('AMS'),
                   Waypoint('LHR'),
                   Waypoint('MCO')])
    aircraft1 = Aircraft("CDG", route)
    aircraft1.departure_time = 10

    route = Route([Waypoint('FRA'),
                   Waypoint('AMS'),
                   Waypoint('LHR'),
                   Waypoint('JFK')])
    aircraft2 = Aircraft("FRA", route)
    aircraft2.departure_time = 0

    aircraft1.fly(8)
    aircraft2.fly(8)
    aircraft1.fly(10)
    aircraft2.fly(10)
    aircraft1.fly(12)
    aircraft2.fly(12)
    aircraft1.fly(16)
    aircraft2.fly(16)
    aircraft1.fly(18)
    aircraft2.fly(18)
    aircraft1.fly(60)
    aircraft2.fly(60)
    aircraft1.fly(79)
    aircraft2.fly(79)
    aircraft1.fly(80)
    aircraft2.fly(80)
    aircraft1.fly(81)
    aircraft2.fly(81)

    #    sim.aircraft.append(aircraft)
#
#    route = Route([Waypoint('FRA'),
#                   Waypoint('AMS'),
#                   Waypoint('LHR'),
#                   Waypoint('JFK')])
#    aircraft = Aircraft("FRA", route)
#    aircraft.departure_time = 0
#    sim.aircraft.append(aircraft)
#
#    sim.execute()

    # docs: http://docs.python.org/library/profile.html
#import cProfile, pstats
#profile_file = 'data/profile.txt'
#cProfile.run('run()', profile_file)
#p = pstats.Stats(profile_file)
#p.strip_dirs()
#p.sort_stats('cumulative')
#p.print_stats(15)