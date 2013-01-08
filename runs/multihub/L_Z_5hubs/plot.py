from ..L_Z_2hubs import plot
import config, os

config.sink_dir = '%s/sink' % os.path.dirname(__file__)
config.count_hubs = 5

def run():
    plot.run()