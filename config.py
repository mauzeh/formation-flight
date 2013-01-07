# Discount factor (@todo rename to beta as in research paper)
alpha = .13

# How much the arrival at the virtual hub can be delayed/expedited (mins)
etah_slack = 5

# How long before hub arrival can we allocate into formations? (mins)
lock_time = 10

# The maximum difference in heading upon hub departure (in degrees)
phi_max = 5

count_hubs = 2
Z = .25

# Departure time distribution
departure_distribution = {
    'type'        : 'uniform',
    'lower_bound' : -10,
    'upper_bound' : 10
}

# Are we in debug mode? Then we are printing a lot of status messages.
from lib import debug
debug.print_severities = [
    #'debug',
    'critical'
]

# Restrictions on formations. Options: 
#   'same-airline',
#   'same-aircraft-type', and
#   None
restrictions = [
    #'same-airline',
    #'same-aircraft-type'
]

# The events we wish to print to the terminal when they occur.
events_printed = [
    #'aircraft-init',
    #'aircraft-depart',
    #'aircraft-at-waypoint',
    #'enter-lock-area',
    #'formation-alive',
    #'aircraft-arrive',
]
