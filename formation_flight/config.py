"""Contains global configuration variables"""

# How much time the arrival at the virtual hub can be delayed/expedited
virtual_hub_arrival_slack = 15

# Which virtual hubs we are employing
# Note that these must be injected in the flight trajectory in advance!
# @todo Should not be necessary to inject in advance.
virtual_hubs = ['AMS', 'EIN']

# Virtual hub assignment algorithm. Can be either "static", 
# "dynamic", or "ad hoc".
# @todo Move this to the data preparation app (which does not exist yet)
hub_assignment = 'static'

# The type of virtual hub. Can be 'point', 'great circle line' or
# 'polygon'. 
# @todo Currently, only 'point' is supported.
hub_type = 'point'

# Formation lock time. How much time before arriving at the hub must a
# formation be locked?
formation_lock_time = 10