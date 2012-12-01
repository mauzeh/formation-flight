"""Allocators determine which hub a given flight should fly to."""

from lib import debug

def allocate(flights, hubs):
    # Assign hubs to flights
    for flight in flights:

        # Find the hub belonging to this route
        hub = get_hub(hubs, flight)

        # Assign hub by injecting into route
        flight.route.waypoints = [
            flight.route.waypoints[0], hub, flight.route.waypoints[1]
        ]

        flight.route.init_segments()

def get_hub(hubs, flight):
    """Assigns a flight to a hub based on the origin for which the hub was
    constructed. All flights leaving from the same airport therefore
    proceed to the same hub."""
    assert len(hubs) > 0
    for hub in hubs:
        for hub_origin in hub.origins:
            if hub_origin.coincides(flight.route.waypoints[0]):
                debug.print_line('Route %s has hub %s' % (
                    flight.route, hub
                ))
                return hub
    raise Exception('Hub not found for flight %s' % flight)
