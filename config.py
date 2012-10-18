# The events we wish to print to the terminal when they occur. Options:
#   'aircraft-depart'
#   'aircraft-at-waypoint'
#   'formation-alive'
#   'aircraft-arrive'
events_printed = ['formation-alive']

# Discount factor
alpha = .13

# How long before hub arrival can we allocate into formations? (mins)
lock_time = 30

# How much the arrival at the virtual hub can be delayed/expedited (mins)
etah_slack = lock_time / 10

# Restrictions on formations. Options: 
#   'same-airline',
#   'same-aircraft-type', and
#   None
restrictions = None

# Generate hubs
from lib.geo.point import Point
hubs = [
    #Point(54.71, -16.29, 'HUB1'),
    #Point(53.22, -17.21, 'HUB2'),
    Point(55.45, -7.9, 'HUB1'),
    Point(52.29, -10.35, 'HUB2'),
    Point(42.46, -5.13, 'HUB3'),
]

# Departure time distribution
departure_distribution = {
    'type'        : 'uniform',
    'lower_bound' : -10,
    'upper_bound' : 10
}