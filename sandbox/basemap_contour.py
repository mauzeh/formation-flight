from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib import mlab
import numpy as np
import math

from mpl_toolkits.axes_grid1 import make_axes_locatable

lats = np.mgrid[ 40: 70: 3j]
lons = np.mgrid[-60: 25: 3j]

lons, lats = np.meshgrid(lons, lats)

data = np.array([
    .5, .6, .7,
    .4, .5, .7,
    .3, .5, .8
])

minlat = np.min(lats)
maxlat = np.max(lats)
minlon = np.min(lons)
maxlon = np.max(lons)

m = Basemap(
    projection = 'merc',
    llcrnrlat = minlat, urcrnrlat = maxlat,
    llcrnrlon = minlon, urcrnrlon = maxlon
)

x = lons
y = lats


z = data

# Reverse Y-axis (high lat = low y)
y = y[::-1]

N = len(z)
print N
nx = math.sqrt(N)
ny = nx

z = z.reshape(nx, ny)

print x
print y
print z

m.drawcoastlines()
m.drawstates()
m.drawcountries()

x, y = m(x, y)
ax = m.contourf(x, y, z)

cb = plt.colorbar()

plt.show()