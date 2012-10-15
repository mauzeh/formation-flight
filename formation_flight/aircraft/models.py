class Aircraft(object):

    def __init__(self, label = None, route = None, departure_time = 0):

        self.label = label if label is not None else str(route)
        self.route = route
        self.description = '%s' % route
        self.departure_time = departure_time
        # Distance units per time unit (500 kts)
        self.speed = 500/60

    def depart(self):
        self.position = self.route.waypoints[0]
        del self.route.waypoints[0]
        pass

    def at_waypoint(self):
        self.position = self.route.waypoints[0]
        del self.route.waypoints[0]
        del self.route.segments[0]
        
    def arrive(self):
        pass

    def time_to_waypoint(self):
        waypoint = self.route.waypoints[0]
        distance = self.position.distance_to(waypoint)
        return distance / self.speed

    def __repr__(self):
        return '%s (%s @ t=%d)' % (self.label, self.route, self.departure_time)
