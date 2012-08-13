from formation_flight.aircraft import Aircraft
from formation_flight.formation import Assigner, Formation
from formation_flight.geo.route import Route
from formation_flight.geo.waypoint import Waypoint
from formation_flight import simulator
from lib.events import EventHandler

if __name__ == '__main__':

    handler = EventHandler()
    assigner = Assigner()

    Waypoint('AMS')
    Waypoint('EIN')

    planes = []

    route = Route([Waypoint('CDG'),
                   Waypoint('AMS'),
                   Waypoint('LHR'),
                   Waypoint('MCO')])
    aircraft = Aircraft("CDG", route)
    aircraft.departure_time = 0
    planes.append(aircraft)

    route = Route([Waypoint('FRA'),
                   Waypoint('AMS'),
                   Waypoint('LHR'),
                   Waypoint('JFK')])
    aircraft = Aircraft("FRA_1", route)
    aircraft.departure_time = 0
    planes.append(aircraft)

    route = Route([Waypoint('FRA'),
                   Waypoint('EIN'),
                   Waypoint('LHR'),
                   Waypoint('JFK')])
    aircraft = Aircraft("FRA_1", route)
    aircraft.departure_time = 0
    planes.append(aircraft)

    route = Route([Waypoint('FRA'),
                   Waypoint('AMS'),
                   Waypoint('LHR'),
                   Waypoint('JFK')])
    aircraft = Aircraft("FRA_2", route)
    aircraft.departure_time = 15
    planes.append(aircraft)

    route = Route([Waypoint('CDG'),
                   Waypoint('AMS'),
                   Waypoint('LHR'),
                   Waypoint('JFK')])
    aircraft = Aircraft("CDG_2", route)
    aircraft.departure_time = 18
    planes.append(aircraft)

    simulator.execute(range(0, 60, 1), planes)

    print '##############################################################'
    print '##############################################################'
    print '##############################################################'
    print '##############################################################'
    print '##############################################################'
    print '##############################################################'

    # docs: http://docs.python.org/library/profile.html
#import cProfile, pstats
#profile_file = 'data/profile.txt'
#cProfile.run('run()', profile_file)
#p = pstats.Stats(profile_file)
#p.strip_dirs()
#p.sort_stats('cumulative')
#p.print_stats(15)