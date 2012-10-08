"""Contains global configuration variables"""

# Hubs that can be assigned to flights.
# @todo Move to data file, and include latlons to allow non-airports as hubs.
hubs = ['MAN']

# How much time the arrival at the virtual hub can be delayed/expedited
virtual_hub_arrival_slack = 15

# Virtual hub assignment algorithm. Can be either "static", 
# "dynamic", or "ad hoc".
# @todo Move this to the data preparation app (which does not exist yet)
hub_assignment = 'static'

# Formation lock time. How much time before arriving at the hub must a
# formation be locked?
formation_lock_time = 20

# Maximum deviation off the reference track (in distance units - NM/km/etc)
max_deviation = 100