import math
from point import Point

def cross_track_distance(d_13, theta_13, theta_12):
    """Calculate distance from great circle path (1 -> 2) to point (3).

    Adapted from http://www.movable-type.co.uk/scripts/latlong.html

    This implementation does not produce a great-circle distance but a mere
    straight-line (through the earth) distance. We don't need anything more
    complicated for our purposes of comparison.

    d_13:     Distance from origin to third point (any distance measure)
    theta_13: Initial bearing from origin to third point (degrees)
    theta_12: Initial bearing from origin to destination (degrees)
    """
    R = 3440
    return math.asin( math.sin (d_13 / R) *\
                      math.sin (math.radians (theta_13 - theta_12))) * R

def midpoint(points):
    """Calculate an average destination based on a planar average (=bad)

    @todo Replace with vectorized version (most accurate solution)
    """
    
    lat_avg = sum(point.lat for point in points) / len(points)
    lon_avg = sum(point.lon for point in points) / len(points)

    return Point(lat_avg, lon_avg)

if __name__ == "__main__":

    print cross_track_distance (34, 237, 187)