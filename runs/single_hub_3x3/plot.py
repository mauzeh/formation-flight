import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
import math
import csv
from mpl_toolkits.basemap import Basemap

data_file = "%s/sink/latest.tsv" % os.path.dirname(__file__)

#print data_file

def get_key(column_name):
    global data_file
    rows = csv.reader(open(data_file, 'rb'), delimiter = "\t")
    for row in rows:
        for column in row:
            if column_name == column:
                return row.index(column)
        break

npdata = np.loadtxt(
    open(data_file, 'rb'),
    delimiter = "\t",
    skiprows = 1
)

#column = 'distance_total'
#column = 'distance_formation'
#column = 'distance_solo'
#column = 'formation_count'
column = 'formation_success_rate'
#column = 'alpha_eff'
#column = 'distance_success_rate'

x = npdata[:, get_key('hub_lon')]
y = npdata[:, get_key('hub_lat')]
z = npdata[:, get_key(column)]

minlat = np.min(y)
maxlat = np.max(y)
minlon = np.min(x)
maxlon = np.max(x)

m = Basemap(
    projection = 'merc', resolution = 'l',
    llcrnrlat = minlat, urcrnrlat = maxlat,
    llcrnrlon = minlon, urcrnrlon = maxlon
)

# Reverse Y-axis (high lat = low y)
#y = y[::-1]

#x, y = np.meshgrid(x, y)

N = len(z)
print N
nx = math.sqrt(N)
ny = nx

x = x.reshape(nx, ny)
y = y.reshape(nx, ny)
z = z.reshape(nx, ny)

print x
print y
print z

m.drawcoastlines()
m.drawstates()
m.drawcountries()

x, y = m(x, y)
m.contourf(x, y, z, 20)

plt.show()