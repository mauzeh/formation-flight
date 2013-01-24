from ..multivariate import plot
from run import get_matrix_dimensions
import config, os

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

def run():
    plot.run()