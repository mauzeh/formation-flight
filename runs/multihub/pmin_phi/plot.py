from ..multivariate import plot
from run import get_matrix_dimensions
import config, os

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

config.axis_x = {
    'name' : r'$P_{min}$',
    'column' : 'config_min_P'
}
config.axis_y = {
    'name' : r'$\phi_{max}$',
    'column' : 'config_phi_max'
}

config.output_nx, config.output_ny = get_matrix_dimensions()

def run():
    plot.run()