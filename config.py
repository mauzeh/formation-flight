# The events we wish to print to the terminal when they occur
# events_printed = ['aircraft-depart', 'aircraft-at-waypoint', 'formation-alive', 'aircraft-arrive']
events_printed = ['formation-alive']

# How much the arrival at the virtual hub can be delayed/expedited (mins)
etah_slack = 5

# How long before hub arrival can we assign into formations? (mins)
lock_time = 10

# Avoid aircraft speed to become unrealistic when synchronizing
assert lock_time >= 2 * etah_slack