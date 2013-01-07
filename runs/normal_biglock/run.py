from ..normal import run
from lib import sink
import config
import os

config.Z = .9

sink.init(os.path.dirname(__file__))

def execute():
    run.execute()