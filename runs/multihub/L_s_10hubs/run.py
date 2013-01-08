from ..L_s_2hubs import run
import config, os

config.sink_dir = '%s/sink' % os.path.dirname(__file__)
config.count_hubs = 10

def execute():
    
    run.execute()