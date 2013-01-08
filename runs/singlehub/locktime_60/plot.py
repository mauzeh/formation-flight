from .. import plot
import config
import os

config.sink_dir = '%s/sink' % os.path.dirname(__file__)

def run():
    plot.run()