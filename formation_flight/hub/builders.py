from lib.geo.util import midpoint
from lib.geo.util import project_segment
from lib.geo.util import reduce_points
from lib.geo.util import point_in_points
from lib.geo.segment import Segment

from lib.util import list_chop

from lib import debug

def build_hubs(planes, count_hubs, Z):

    routes = []
    for flight in planes:
        routes.append(flight.route)

    hubs         = []
    origins      = []
    destinations = []
    for route in routes:
        origins.append(route.waypoints[0])
        destinations.append(route.waypoints[-1])

    origins      = reduce_points(origins)
    destinations = reduce_points(destinations)

    origins_ranked = rank_origins(origins, destinations)
    origin_chunks  = list_chop(origins_ranked, count_hubs)

    debug.print_line('Origin count: %d' % len(origins_ranked))
    debug.print_line('Hubs required: %d' % count_hubs)
    debug.print_line('Chunk count: %d' % len(origin_chunks))

    od_chunks = []
    for origin_chunk in origin_chunks:

        # Construct weighted list of destinations belonging to origin chunk
        destination_chunk = []
        for route in routes:
            if not point_in_points(route.waypoints[0], origin_chunk):
                continue
            destination_chunk.append(route.waypoints[-1])
        destination_chunk = reduce_points(destination_chunk)
        od_chunks.append((origin_chunk, destination_chunk))

    for od_chunk in od_chunks:

        #hub_segment = Segment(
        #    construct_hub(origin_chunk, destination_chunk, Z = 0),
        #    construct_hub(origin_chunk, destination_chunk, Z = 1))

        hub = construct_hub(
            origins = reduce_points(od_chunk[0]),
            destinations = reduce_points(od_chunk[1]),
            Z = Z)

        hub.name = 'HUB%02d' % od_chunks.index(od_chunk)
        hubs.append(hub)

    for hub in hubs:
        debug.print_line('Hub %s created at %s' % (
            hub, "%d, %d" % (
                hub.lat, hub.lon
            )
        ))
        debug.print_line('Hub %s has %d origins %s' % (
            hub, len(hub.origins), hub.origins
        ))
    return hubs

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