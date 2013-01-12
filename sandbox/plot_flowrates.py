import numpy as np
import matplotlib.pyplot as plt
import math

def plot_flow_rate(data):

    timestamps = []
    values     = []
    
    for key in sorted(data.iterkeys()):
        timestamps.append(key)
        values.append(data[key])
    
    # For testing/debugging
    #timestamps = np.arange(0, 1440, 60)
    #values = np.linspace(0, 35, len(timestamps))

    time_labels = []

    for timestamp in timestamps:
    
        # Normalize time to be reset after midnight (if > 1440, then subtract 1440)
        timestamp = timestamp % 1440
        hours     = math.floor(timestamp / 60)
        minutes   = math.floor(timestamp - hours * 60)
        
        time_labels.append('%02d:%02d' % (hours, minutes))
    
    plt.rc(('xtick.major', 'ytick.major'), pad = 10)
    
    plt.bar(
        timestamps,
        values,
        width = 50,
        linewidth = 0,
        color = '#999999'
    )
    
    plt.xlim(0, 1440)
    
    plt.xticks(
        [0, 180, 360, 540, 720, 1440],
        ['00:00', '03:00', '06:00', '09:00', '12:00', '00:00']
    )
    
    plt.show()

data = {
      0: 0,
     60: 40,
    120: 30,
    180: 12,
    240: 55,
    300: 21
}

plot_flow_rate(data)