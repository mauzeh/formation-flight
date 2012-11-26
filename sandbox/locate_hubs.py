from formation_flight.aircraft.models import Aircraft

from lib.geo.util import midpoint
from lib.geo.util import project_segment
from lib.geo.util import reduce_points
from lib.geo.util import point_in_points

from lib.util import list_chop

from lib.geo.point import Point
from lib.geo.waypoint import Waypoint
from lib.geo.segment import Segment
from lib.geo.route import Route
from lib.geo.visualization import GCMapper

def construct_hub(origins, destinations, Z):

    midpoint_origins      = midpoint(origins)
    midpoint_destinations = midpoint(destinations)
    
    hub_route = Segment(midpoint_origins, midpoint_destinations)
    hub = hub_route.start.get_position(
        hub_route.get_initial_bearing(),
        hub_route.get_length() * Z
    )
    
    hub.origins      = origins
    hub.destinations = destinations
    
    return hub

def rank_origins(origins, destinations):

    midpoint_origins = midpoint(origins)
    midpoint_destinations = midpoint(destinations)
    hub_route = Segment(midpoint_origins, midpoint_destinations)
    for origin in origins:
        
        AC = Segment(midpoint_origins, origin)
        orthogonal_heading = hub_route.get_initial_bearing() + 90    
        (a, b) = project_segment(
            abs(orthogonal_heading - AC.get_initial_bearing()),
            AC.get_length()
        )
        projection = midpoint_origins.get_position(
            orthogonal_heading, a
        )
        midpoint_to_projection = Segment(
            midpoint_origins,
            projection
        )
        
        angle = abs(
            hub_route.get_initial_bearing() - 
            midpoint_to_projection.get_initial_bearing()
        )
        if abs(angle - 90) < 0.1:
            distance = -1 * midpoint_to_projection.get_length()
        else:
            distance = midpoint_to_projection.get_length()
        origin.distance_to_midpoint = distance
        
    return sorted(origins, key = lambda point: point.distance_to_midpoint)

def get_hub_by_flight(hubs, flight):
    for hub in hubs:
        for hub_origin in hub.origins:
            if hub_origin.coincides(flight.route.waypoints[0]):
                return hub
    raise Exception('Hub not found for flight %s' % flight)

def build_hubs(flights, count_hubs, Z):
    
    origins      = []
    destinations = []

    for flight in flights:
        origins.append(flight.route.waypoints[0])
        destinations.append(flight.route.waypoints[1])

    origins      = reduce_points(origins)
    destinations = reduce_points(destinations)

    origins_ranked = rank_origins(origins, destinations)
    origin_chunks  = list_chop(origins_ranked, count_hubs)
    
    od_chunks = []
    for origin_chunk in origin_chunks:

        # Construct weighted list of destinations belonging to origin chunk
        destination_chunk = []
        for flight in flights:
            if not point_in_points(flight.route.waypoints[0], origin_chunk):
                continue
            destination_chunk.append(flight.route.waypoints[1])
        destination_chunk = reduce_points(destination_chunk)
        od_chunks.append((origin_chunk, destination_chunk))

    hubs = []
    for od_chunk in od_chunks:

        #hub_segment = Segment(
        #    construct_hub(origin_chunk, destination_chunk, Z = 0),
        #    construct_hub(origin_chunk, destination_chunk, Z = 1))

        hub = construct_hub(
            origins = od_chunk[0],
            destinations = od_chunk[1],
            Z = Z)
        
        hubs.append(hub)

    return hubs

def run():

    count_hubs = 2
    Z = .3
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

    hubs = build_hubs(planes, count_hubs, .1)
    
    for plane in planes:
        
        # Find the hub belonging to this flight
        hub = get_hub_by_flight(hubs, plane)
        
        # Assign hub by injecting into route
        plane.route.waypoints = [plane.route.waypoints[0],
                                 hub,
                                 plane.route.waypoints[1]]

    viz = GCMapper()
    for plane in planes:
        viz.plot_route(plane.route)
        viz.plot_point(plane.route.waypoints[0])
        viz.plot_point(plane.route.waypoints[-1])

    for hub in hubs:
        viz.plot_point(hub, formatting = 'bo')

    viz.render()