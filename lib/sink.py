"""Captures data and puts it into data/output.tsv"""
import csv
from lib import sim

from formation_flight import statistics

writer = None

# Only print the header once. Useful when running the sim multiple times.
print_header = True

def init():
    global writer
    writer = csv.writer(open('data/sink.tsv', 'w'), delimiter = '\t')
    sim.dispatcher.register('sim-finish', execute)

def execute(event):
    global writer, print_header
    if print_header == True:
        writer.writerow(statistics.vars.keys())
    writer.writerow(statistics.vars.values())
    print_header = False
