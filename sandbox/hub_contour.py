import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
import math
import csv
from mpl_toolkits.basemap import Basemap

data_file = "../data/sink.tsv"

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
#column = 'formation_success_rate'
#column = 'alpha_eff'
#column = 'distance_success_rate'
column = 'formation_success_rate'

x = npdata[:, get_key('hub_lon')]
y = npdata[:, get_key('hub_lat')]
z = npdata[:, get_key(column)]

print x
print y
print z

N = len(x)
nx = math.sqrt(N)
ny = nx

x = x.reshape(nx, ny)
y = y.reshape(nx, ny)
z = z.reshape(nx, ny)

plt.figure()
plt.contourf(x, y, z, 20)
plt.contour(x, y, z, 20)
plt.colorbar()
plt.title(column)
#plt.show()
