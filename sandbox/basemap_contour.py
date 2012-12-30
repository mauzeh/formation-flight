from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib import mlab
import numpy as np

# More Info: http://davydany.com/post/32287214449/matplotlibs-basemap-plotting-a-list-of-latitude
def show_map(a):



    # 'a' is of the format [(lats, lons, data), (lats, lons, data)... (lats, lons, data)]
    lats = [ x[0] for x in a ]
    lons = [ x[1] for x in a ]
    data = [ x[2] for x in a ]
     
    lat_min = min(lats)
    lat_max = max(lats)
    lon_min = min(lons)
    lon_max = max(lons)
    data_min = min(data)
    data_max = max(data)


    m = Basemap(
        projection = 'merc',
        llcrnrlat=lat_min, urcrnrlat=lat_max,
        llcrnrlon=lon_min, urcrnrlon=lon_max,
        rsphere=6371200., resolution='l', area_thresh=10000
    )

    spatial_resolution = 0.5
    fig = plt.figure()

    x = np.array(lats)
    y = np.array(lons)
    z = np.array(data)
   
    xinum = (lat_max - lat_min) / spatial_resolution
    yinum = (lon_max - lon_min) / spatial_resolution
    xi = np.linspace(lat_min, lat_max + spatial_resolution, xinum)        # same as [lat_min:spatial_resolution:lat_max] in matlab
    yi = np.linspace(lon_min, lon_max + spatial_resolution, yinum)        # same as [lon_min:spatial_resolution:lon_max] in matlab
    xi, yi = np.meshgrid(xi, yi)
   
    zi = mlab.griddata(x, y, z, xi, yi)
   
    lat, lon = m.makegrid(zi.shape[1], zi.shape[0])
    x,y = m(lat, lon)

    m.contourf(x, y, zi)
    cs = m.contour(x, y, zi)

    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    
    plt.clabel(cs, fmt = '%.0f', inline = True)   
    plt.show()

show_map([
    (10.,  9., 15.),
    (11., 11., 17.),
    (12., 11., 17.),
    (13., 11., 17.),
    (14., 11., 17.),
    (15., 11., 17.),
    (16., 11., 17.),
    (17., 11., 17.),
    (18., 11., 17.),
    (19., 11., 17.),
    (20., 11., 17.),
    (21., 11., 17.),
    (21., 11., 17.),
    (22., 15., 16.),
    (23., 14., 12.),
    (24., 12., 11.),
    (25., 13., 1.),
])