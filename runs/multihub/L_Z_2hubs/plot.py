from ..multivariate import plot
import config, os

config.sink_dir = '%s/sink' % os.path.dirname(__file__)
config.count_hubs = 2

config.axis_x = {
    'name' : r'$Z$',
    'column' : 'config_Z'
}

def run():
    plot.run()