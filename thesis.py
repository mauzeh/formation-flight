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
    sim.time = range(0, 120, 1)

    route = Route([Waypoint('CDG'),
                   Waypoint('AMS'),
                   Waypoint('LHR'),
                   Waypoint('MCO')])
    aircraft = Aircraft("CDG", route)
    aircraft.departure_time = 0
    sim.aircraft.append(aircraft)

    route = Route([Waypoint('FRA'),
                   Waypoint('AMS'),
                   Waypoint('LHR'),
                   Waypoint('MCO')])
    aircraft = Aircraft("FRA", route)
    aircraft.departure_time = 0
    sim.aircraft.append(aircraft)

    route = Route([Waypoint('BRU'),
                   Waypoint('AMS'),
                   Waypoint('LHR'),
                   Waypoint('JFK')])
    aircraft = Aircraft("BRU", route)
    aircraft.departure_time = 15
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