# The events we wish to print to the terminal when they occur
# events_printed = ['aircraft-depart', 'aircraft-at-waypoint', 'formation-alive', 'aircraft-arrive']
events_printed = ['formation-alive']#, 'aircraft-arrive']

# How long before hub arrival can we allocate into formations? (mins)
lock_time = 10

# How much the arrival at the virtual hub can be delayed/expedited (mins)
etah_slack = lock_time / 10