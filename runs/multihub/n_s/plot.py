from ..multivariate import plot
import config, os

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

config.axis_x = {
    'name' : r'$n$',
    'column' : 'config_count_hubs'
}
config.axis_y = {
    'name' : r'$s$',
    'column' : 'config_s'
}

config.output_nx = 5
config.output_ny = 20

def run():
    plot.run()