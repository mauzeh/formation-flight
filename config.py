# Discount factor (@todo rename to beta as in research paper)
alpha = .13

# How much the arrival at the virtual hub can be delayed/expedited (mins)
etah_slack = 7

# How long before hub arrival can we allocate into formations? (mins)
lock_time = 60

# The maximum difference in heading upon hub departure (in degrees)
phi_max = 1

# The amount of hubs in the system
count_hubs = 5

# A measure for how far the hub is away from the origin
Z = .14

# Departure time distribution bound (becomes param for uniform(-,+))
dt = 10

# If flight list was calibrated, set a selection criterium for the formation
# probability here
min_P = .5

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
    'critical'
]