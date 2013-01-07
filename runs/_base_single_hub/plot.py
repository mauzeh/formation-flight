import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
import math
import csv
from lib.util import make_sure_path_exists
from mpl_toolkits.basemap import Basemap
import config

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

config.plots = [
    {
        'column' : 'formation_count',
        'title'  : r'Formation Count $M$',
        'levels' : np.arange(0, 140, 10),
    },{
        'column' : 'formation_success_rate',
        'title'  : r'Formation Success Rate $S_f$',
        'levels' : np.arange(0, 1.05, .05),
    },{
        'column' : 'alpha_eff',
        'title'  : r'Effective Discount $\alpha_{eff}$',
        'levels' : np.arange(-.5, config.alpha, .025),
    },{
        'column' : 'distance_success_rate',
        'title'  : r'Distance Success Rate $S_d$',
        'levels' : np.arange(0, 1.05, .05),
    },{
        'column' : 'fuel_saved',
        'title'  : r'Fuel Saved',
        'levels' : 20,
    },{
        'column' : 'distance_penalty',
        'title'  : r'Distance Penalty $P_d$',
        'levels' : np.arange(0, 1.05, .05),
    }
]

#config.output_var = 'distance_total'
#config.output_var = 'distance_formation'
#config.output_var = 'distance_solo'
#config.output_var = 'formation_count'
#config.output_var = 'formation_success_rate'
#config.output_var = 'alpha_eff'
#config.output_var = 'distance_success_rate'

#config.contour_levels = np.arange(.8, 1, .05)

#print data_file

def get_key(column_name):
    
    data_file = '%s/latest.tsv' % config.sink_dir

    rows = csv.reader(open(data_file, 'rb'), delimiter = "\t")
    for row in rows:
        for column in row:
            if column_name == column:
                return row.index(column)
        break

def run():
    
    data_file = '%s/latest.tsv' % config.sink_dir
    
    data = np.loadtxt(
        open(data_file, 'rb'),
        delimiter = "\t",
        skiprows = 1
    )
    
    for plotconf in config.plots:
        do_plot(plotconf, data)
    
def do_plot(plotconf, data):
    
    plt.figure()
    
    column = plotconf['column']
    print 'Drawing plot for %s' % column
    
    x = data[:, get_key('hub_lon')]
    y = data[:, get_key('hub_lat')]
    z = data[:, get_key(column)]
    
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
    #print N
    nx = math.sqrt(N)
    ny = nx
    
    x = x.reshape(nx, ny)
    y = y.reshape(nx, ny)
    z = z.reshape(nx, ny)

    #print x
    #print y
    #print z
    
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    
    x, y = m(x, y)
    m.contourf(x, y, z, plotconf['levels'])
    
    plt.colorbar()
    plt.title(plotconf['title'])
    
    #plt.show()
    
    fig_path = '%s/plot_%s.pdf' % (config.sink_dir, column)
    fig_path = fig_path.replace('/runs/', '/plots/')
    fig_path = fig_path.replace('/sink/', '/')
    make_sure_path_exists(os.path.dirname(fig_path))
    plt.savefig(fig_path)
    