from .._base_multiple_hub import run
from lib import sink
import config
import os

config.lock_time = 30
config.count_hubs = 5

config.sink_path = os.path.dirname(__file__)

def execute():
    run.execute()