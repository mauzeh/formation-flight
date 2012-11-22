# The events we wish to print to the terminal when they occur.
events_printed = [
    #'aircraft-init',
    #'aircraft-depart',
    #'aircraft-at-waypoint',
    #'enter-lock-area',
    'formation-alive',
    #'aircraft-arrive',
]

# The maximum difference in heading upon hub departure (in degrees)
phi_max = 3

# The slack ramp (in time units per distance unit away from the hub)
psi = .132

# Discount factor (@todo rename to beta as in research paper)
alpha = .13

# How long before hub arrival can we allocate into formations? (mins)
lock_time = 30

# How much the arrival at the virtual hub can be delayed/expedited (mins)
etah_slack = 5

# How large is a formation allowed to be
S_max = 100

# Restrictions on formations. Options: 
#   'same-airline',
#   'same-aircraft-type', and
#   None
restrictions = None

# Generate hubs
# Visualization:
# http://www.gcmap.com/mapui?P=63N+10W%0D%0A58N+11W%0D%0A53N+12.3W%0D%0A48N+13.6W%0D%0A43N+15W%0D%0Alhr-bos%0D%0Aams-atl%0D%0Ahel-jfk%0D%0Amad-dca&MS=wls&DU=mi
from lib.geo.point import Point
from lib.geo.waypoint import Waypoint
hubs = [
    #Waypoint('MAN')
    Point(63, -10, 'HUB1'),
    Point(58, -11, 'HUB2'),
    Point(53, -12.3, 'HUB3'),
    Point(48, -13.6, 'HUB4'),
    Point(43, -15, 'HUB5'),
]

# Departure time distribution
departure_distribution = {
    'type'        : 'uniform',
    'lower_bound' : -10,
    'upper_bound' : 10
}