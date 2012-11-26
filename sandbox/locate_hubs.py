from formation_flight.aircraft.models import Aircraft

from lib.geo.waypoint import Waypoint
from lib.geo.route import Route
from lib.geo.visualization import GCMapper

from formation_flight.hub.builders import Builder

import config

def run():

    planes = [
        Aircraft('FLT001', Route([Waypoint('AMS'), Waypoint('JFK')]), 12),
        Aircraft('FLT001', Route([Waypoint('AMS'), Waypoint('ORD')]), 12),
        Aircraft('FLT001', Route([Waypoint('AMS'), Waypoint('EWR')]), 12),
        Aircraft('FLT002', Route([Waypoint('DUS'), Waypoint('BOS')]), 12),
        Aircraft('FLT003', Route([Waypoint('FRA'), Waypoint('EWR')]), 0),
        Aircraft('FLT004', Route([Waypoint('BRU'), Waypoint('LAX')]), 11),
        Aircraft('FLT005', Route([Waypoint('AMS'), Waypoint('SFO')]), 7),
        Aircraft('FLT007', Route([Waypoint('AMS'), Waypoint('LAX')]), 100),
        Aircraft('FLT008', Route([Waypoint('BRU'), Waypoint('SFO')]), 100),
        Aircraft('FLT009', Route([Waypoint('CDG'), Waypoint('LAX')]), 100),
    ]
    
    routes = []
    for flight in planes:
        routes.append(flight.route)

    builder = Builder(routes)
    builder.build_hubs(config.count_hubs, config.Z)
    
    for flight in planes:
        
        # Find the hub belonging to this route
        hub = builder.get_hub_by_route(flight.route)
        
        # Assign hub by injecting into route
        flight.route.waypoints = [flight.route.waypoints[0],
                                  hub,
                                  flight.route.waypoints[1]]

    #viz = GCMapper()
    #for plane in planes:
    #    viz.plot_route(plane.route)
    #    viz.plot_point(plane.route.waypoints[0])
    #    viz.plot_point(plane.route.waypoints[-1])
    #
    #for hub in builder.hubs:
    #    viz.plot_point(hub, formatting = 'bo')
    #
    #viz.render()