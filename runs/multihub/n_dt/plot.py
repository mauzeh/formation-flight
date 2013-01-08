from ..multivariate import plot
import config, os

config.sink_dir = '%s/sink' % os.path.dirname(__file__)
config.count_hubs = 2

config.axis_x = {
    'name' : r'$n$',
    'column' : 'config_count_hubs'
}
config.axis_y = {
    'name' : r'$dt$',
    'column' : 'config_dt'
}

config.output_nx = 19
config.output_ny = 46

def run():
    plot.run()