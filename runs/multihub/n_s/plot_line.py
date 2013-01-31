import config
from lib.util import tsv_get_column_index
from run import get_matrix_dimensions
import os
import math
from lib.util import make_sure_path_exists

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

config.axis_x = {
    'name' : r'$H$',
    'column' : 'config_count_hubs'
}
config.axis_y = {
    'name' : r'$s$',
    'column' : 'config_etah_slack'
}

config.output_nx, config.output_ny = get_matrix_dimensions()

config.interesting_z_axes = [{
    'name' : 'Average Formation Size',
    'column' : 'avg_formation_size'
}]

def run():
    
    data_file = '%s/latest.tsv' % config.sink_dir
    
    data = np.loadtxt(
        open(data_file, 'rb'),
        delimiter = "\t",
        skiprows = 1
    )

    axis_x = config.axis_x
    axis_y = config.axis_y

    for axis_z in config.interesting_z_axes:
        
        plt.figure()
    
        x = data[:, tsv_get_column_index(data_file, axis_x['column'])]
        y = data[:, tsv_get_column_index(data_file, axis_y['column'])]
        z = data[:, tsv_get_column_index(data_file, axis_z['column'])]
        
        # Note that we must convert the lock time into the lock distance L
        if axis_x['column'] == 'config_lock_time':
            x = 300 * x / 60
        if axis_y['column'] == 'config_lock_time':
            y = 300 * y / 60

        try:
            nx = config.output_nx
            ny = config.output_ny
        except AttributeError:
            N = len(z)
            nx = math.sqrt(N)
            ny = nx
        #    
        #print 'variable: %s, nx = %d, ny = %d, count z = %d. z = %s' % (
        #    axis_z['column'],
        #    nx, ny, len(z), z
        #)

        x = x.reshape(nx, ny)
        y = y.reshape(nx, ny)
        z = z.reshape(nx, ny)
        
        plt.xlabel(axis_x['name'])
        plt.ylabel(axis_y['name'])
        
        print x,y,z
        print x[:,0]
        print y[0,:]
        print z[0,:]
        
        plt.plot(y[0,:],z[0,:])
        plt.show()
        return
        
        plt.grid(True)
        
        try:
            cs = plt.contour(x, y, z, axis_z['levels'])
        except KeyError:
            cs = plt.contour(x, y, z, 10)

        plt.clabel(cs)
        
        plt.colorbar()
        
        #plt.title(r'%s ($n=%d$)' % (axis_z['name'], config.count_hubs))
        plt.title(r'%s' % axis_z['name'])
        
        fig_path = '%s/plot_%s.pdf' % (config.sink_dir, axis_z['column'])
        fig_path = fig_path.replace('/runs/', '/plots/')
        fig_path = fig_path.replace('/sink/', '/')
        make_sure_path_exists(os.path.dirname(fig_path))
        #plt.show()
        #plt.savefig(fig_path)


