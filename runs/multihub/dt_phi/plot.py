from ..multivariate import plot
from run import get_matrix_dimensions
import config, os

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

config.axis_x = {
    'name' : r'$n$',
    'column' : 'config_count_hubs'
}
config.axis_y = {
    'name' : r'$\sigma$',
    'column' : 'config_dt'
}

config.output_nx, config.output_ny = get_matrix_dimensions()

def run():
    plot.run()