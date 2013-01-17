from ..multivariate import plot
from run import get_matrix_dimensions
import config, os

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

config.axis_x = {
    'name' : r'$L$',
    'column' : 'config_lock_time'
}
config.axis_y = {
    'name' : r'$Z$',
    'column' : 'config_Z'
}

config.output_nx, config.output_ny = get_matrix_dimensions()

def run():
    plot.run()