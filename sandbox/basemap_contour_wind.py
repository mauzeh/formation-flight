from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

np.set_printoptions(precision=3)

m = Basemap(projection = 'ortho',lat_0 = 40, lon_0 = -80)
m.drawmapboundary(fill_color = 'white')
m.drawcoastlines(color = 'black',linewidth = 0.5)
m.fillcontinents(color = '0.85')
m.drawparallels(np.arange(-90, 91,30), color = '0.25', linewidth = 0.5)
m.drawmeridians(np.arange(-180,180,30), color = '0.25', linewidth = 0.5)
data = np.load('basemap_contour/contour_sample.npz')

print data['lon']
print data['lat']
print data['z']

lon = data['lon'] 
lat = data['lat'] 
z = data['z'] 
x,y = m(lon,lat) 
cs = m.contour(x,y,z, levels = range(-180,360,30),colors = 'blue')
plt.clabel(cs, fmt = '%.0f', inline = True)
plt.show() 