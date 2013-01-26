import config
from lib.util import tsv_get_column_index
import os
import math
from lib.util import make_sure_path_exists

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

config.axis_x = {
    'name' : r'Slack $s$',
    'column' : 'config_etah_slack'
}
config.axes_y = [{
    'name' : 'Distance Penalty',
    'column' : 'distance_penalty'
},{
    'name' : r'Distance Flown [NM]',
    'column' : 'distance_total',
},{
    'name' : r'Distance Success Rate $S_d$',
    'column' : 'distance_success_rate',
},{
    'name' : r'Formation Success Rate $S_f$',
    'column' : 'formation_success_rate'
},{
    'name' : 'Average Formation Size',
    'column' : 'avg_formation_size'
},{
    'name' : 'Formation Count',
    'column' : 'formation_count'
},{
    'name' : 'Fuel Saved [%]',
    'column' : 'fuel_saved'
},{
    'name' : 'Fuel Saved [kg]',
    'column' : 'fuel_saved_abs'
},{
    'name' : 'Fuel Saved (Without Delay Costs)',
    'column' : 'fuel_saved_disregard_delay'
},{
    'name' : 'Average Hub Delay [min]',
    'column' : 'hub_delay_avg'
},{
    'name' : 'Delay Fuel [kg]',
    'column' : 'fuel_delay'
},{
    'name' : r'$Q_{avg}$',
    'column' : 'Q_avg'
},{
    'name' : 'Delay Fuel [kg]',
    'column' : 'fuel_delay'
}]

font = {'size' : 24}
matplotlib.rc('font', **font)

def run():
    
    data_file = '%s/latest.tsv' % config.sink_dir
    
    data = np.loadtxt(
        open(data_file, 'rb'),
        delimiter = "\t",
        skiprows = 1
    )
    
    j = 0
    for axis_y in config.axes_y:
        
        print 'Plotting %s (%d of %d)' % (
            axis_y['column'], (j+1), len(config.axes_y)
        )
        
        axis_x = config.axis_x
    
        fig = plt.figure(j)
        ax  = fig.add_subplot(111)
    
        x = data[:, tsv_get_column_index(data_file, axis_x['column'])]
        y = data[:, tsv_get_column_index(data_file, axis_y['column'])]
        
        # Note that we must convert the lock time into the lock distance L
        if axis_x['column'] == 'config_lock_time':
            raise Error('lock time needs conversion')
        
        nx = len(config.x)
        ny = len(config.y)
    
        #    
        #print 'variable: %s, nx = %d, ny = %d, count z = %d. z = %s' % (
        #    axis_z['column'],
        #    nx, ny, len(z), z
        #)
        #
        x = x.reshape(nx, ny)
        y = y.reshape(nx, ny)
        
        plt.xlabel(axis_x['name'])
        plt.ylabel(axis_y['name'])
        
        i = 0
        for line in config.x:

            if axis_x['column'] == 'config_dt':
                horizontal = x[0,:] / 20
            else:
                horizontal = x[0,:]

            plt.plot(horizontal, y[i,:], label = r'$H=%d$' % line)
            i += 1
    
        plt.grid(True)
        plt.title(r'%s' % axis_y['name'])
        lgd = ax.legend(
            loc='upper center',
            bbox_to_anchor=(0.5,-0.15),
            ncol = 2
        )
        fig.savefig(
            'samplefigure.pdf',
            bbox_extra_artists=(lgd,),
            bbox_inches='tight'
        )

        fig_path = '%s/plot_%s.pdf' % (config.sink_dir, axis_y['column'])
        fig_path = fig_path.replace('/runs/', '/plots/')
        fig_path = fig_path.replace('/sink/', '/')
        make_sure_path_exists(os.path.dirname(fig_path))
        plt.savefig(
            fig_path,
            bbox_extra_artists=(lgd,),
            bbox_inches='tight'
        )
        
        j += 1
    

