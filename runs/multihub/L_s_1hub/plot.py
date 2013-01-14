from ..multivariate import plot
import config, os

config.sink_dir = '%s/sink' % os.path.dirname(__file__)
config.count_hubs = 1

config.axis_x = {
    'name' : 'Slack',
    'column' : 'config_etah_slack'
}

def run():
    plot.run()