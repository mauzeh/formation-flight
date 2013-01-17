# Discount factor (@todo rename to beta as in research paper)
alpha = .13

# How much the arrival at the virtual hub can be delayed/expedited (mins)
etah_slack = 7

# How long before hub arrival can we allocate into formations? (mins)
lock_time = 20

# The maximum difference in heading upon hub departure (in degrees)
phi_max = 5

# The amount of hubs in the system
count_hubs = 1

# A measure for how far the hub is away from the origin
Z = .17

# Departure time distribution bound (becomes param for uniform(-,+))
dt = 10

# If flight list was calibrated, use this value as the selection criterium for
# the minimum formation required probability
min_P = 0.8

# Mainly used for validation. One way in which validation is performed is by
# comparing the simulation output to a manual calculation. Having a single
# aircraft model makes this a bit easier.
model = {
    'name' : 'B772',
    'V'    : 500,
    'c_L'  : .6,
    'L_D'  : 17,
    #'W_1' : 297550 - 14000 # B777 Maxweight at start of cruise
    'W_1'  : 300000
}

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

# Are we in debug mode? Then we are printing a lot of status messages.
from lib import debug
debug.print_severities = [
    #'debug',
    #'validate',
    #'geo-debug',
    #'warning',
    'critical',
    'new'
]